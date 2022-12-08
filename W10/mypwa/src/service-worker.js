import { build, files, version } from '$service-worker';
 
// Create a unique cache name for this deployment
const CACHE = `cache-${version}`;
 
const ASSETS = [
  ...build, // the app itself
  ...files  // everything in `static`
];
 
self.addEventListener('install', (event) => {
  console.info('[ServiceWorker] Installed')
  // Create a new cache and add all files to it
  async function addFilesToCache() {
    const cache = await caches.open(CACHE);
    await cache.addAll(ASSETS);
  }
 
  event.waitUntil(addFilesToCache());
});
 
self.addEventListener('activate', (event) => {
  console.info('[ServiceWorker] Activated')
  // Remove previous cached data from disk
  async function deleteOldCaches() {
    for (const key of await caches.keys()) {
      if (key !== CACHE) await caches.delete(key);
    }
  }
 
  event.waitUntil(deleteOldCaches());
});
 
self.addEventListener('fetch', (event) => {
  console.info('[ServiceWorker]', event.request.method, event.request.url, '...');

  // ignore POST requests etc
  if (event.request.method !== 'GET') {
    console.info('Skipped not-GET method');
    return;
  }
  
  async function respond() {
    const url = new URL(event.request.url);
    const cache = await caches.open(CACHE);
 
    // `build`/`files` can always be served from the cache
    if (ASSETS.includes(url.pathname)) {
      return cache.match(event.request);
    }
 
    // for everything else, try the network first, but
    // fall back to the cache if we're offline
    try {
      const response = await fetch(event.request);
 
      if (response.status === 200) {
        cache.put(event.request, response.clone());
      }
 
      return response;
    } catch {
      return cache.match(event.request);
    }
  }
 
  event.respondWith(respond());
});

// based on: http://github.com/mdn/serviceworker-cookbook/tree/master/request-deferrer
function tryOrFallback(fakeResponse) {
	return function(req, res) {
		// If offline, enqueue and answer with the fake response.
		if (!navigator.onLine) {
			console.info('[ServiceWorker] No network availability, enqueuing');
			return enqueue(req).then(function() {
				// As the fake response will be reused but Response objects
				// are one use only, we need to clone it each time we use it.
				return fakeResponse.clone();
			});
		}
		
		// If online, flush the queue and answer from network.
		console.info('[ServiceWorker] Network available! Flushing queue.');
		return flushQueue().then(function() {
			return fetch(req);
		});
	};
}

// Serialize is a little bit convolved due to headers is not a simple object.
function serialize(request) {
	var headers = {};
	// `for(... of ...)` is ES6 notation but current browsers supporting SW, support this
	// notation as well and this is the only way of retrieving all the headers.
	for (var entry of request.headers.entries()) {
		headers[entry[0]] = entry[1];
	}
	var serialized = {
		url: request.url,
		headers: headers,
		method: request.method,
		mode: request.mode,
		credentials: request.credentials,
		cache: request.cache,
		redirect: request.redirect,
		referrer: request.referrer
	};
	
	// Only if method is not `GET` or `HEAD` is the request allowed to have body.
	if (request.method !== 'GET' && request.method !== 'HEAD') {
		return request.clone().text().then(function(body) {
			serialized.body = body;
			return Promise.resolve(serialized);
		});
	}
	return Promise.resolve(serialized);
}

function deserialize(data) {
	return Promise.resolve(new Request(data.url, data));
}

// Enqueue consists of adding a request to the list. Due to the
// limitations of IndexedDB, Request and Response objects can not
// be saved so we need an alternative representations. This is
// why we call to `serialize()`.`
function enqueue(request) {
	return serialize(request).then(function(serialized) {
		localforage.getItem('queue').then(function(queue) {
			/* eslint no-param-reassign: 0 */
			queue = queue || [];
			queue.push(serialized);
			return localforage.setItem('queue', queue).then(function() {
				console.log(serialized.method, serialized.url, 'enqueued!');
			});
		});
	});
}

// Flush is a little more complicated. It consists of getting
// the elements of the queue in order and sending each one,
// keeping track of not yet sent request. Before sending a request
// we need to recreate it from the alternative representation
// stored in IndexedDB.
function flushQueue() {
	return localforage.getItem('queue').then(function(queue) {
		/* eslint no-param-reassign: 0 */
		queue = queue || [];
		
		// If empty, nothing to do!
		if (!queue.length) {
			return Promise.resolve();
		}
		
		// Else, send the requests in order...
		console.log('Sending ', queue.length, ' requests...');
		return sendInOrder(queue).then(function() {
			// **Requires error handling**. Actually, this is assuming all the requests
			// in queue are a success when reaching the Network. So it should empty the
			// queue step by step, only popping from the queue if the request completes
			// with success.
			return localforage.setItem('queue', []);
		});
	});
}

// Send the requests inside the queue in order. Waiting for the current before
// sending the next one.
function sendInOrder(requests) {
	// The `reduce()` chains one promise per serialized request, not allowing to
	// progress to the next one until completing the current.
	var sending = requests.reduce(function(prevPromise, serialized) {
		console.log('[ServiceWorker] Sending', serialized.method, serialized.url);
		return prevPromise.then(function() {
			return deserialize(serialized).then(function(request) {
				return fetch(request);
			});
		});
	}, Promise.resolve());
	return sending;
}
