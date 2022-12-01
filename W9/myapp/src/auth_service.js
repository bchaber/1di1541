import { get } from 'svelte/store';
import { createAuth0Client } from '@auth0/auth0-spa-js';
import { user, authenticated, authorized, popup, token } from './store';
import config from '../auth_config';

async function createClient() {
  let client = await createAuth0Client({
    domain: config.domain,
    clientId: config.clientId
  });
  return client;
}

async function loginWithPopup(client) {
  popup.set(true);
  try {
    await client.loginWithPopup();

    user.set(await client.getUser());
    authenticated.set(true);

    console.info("Logged in as: ");
    console.info(get(user));
  } catch (e) {
    console.error(e);
  } finally {
    popup.set(false);
  }
}

async function authorizeWithPopup(client) {
  popup.set(true);
  try {
    token.set(await client.getTokenWithPopup({
      authorizationParams: {
        audience: 'http://localhost:3001',
        scope: 'read:tasks write:tasks'
      }
    }));
    authorized.set(true);

    console.info("Access token for API: ");
    console.info(get(token));
  } catch (e) {
    console.error(e);
  } finally {
    popup.set(false);
  }
}

function logout(client) {
  return client.logout();
}

const auth = {
  createClient,
  authorizeWithPopup,
  loginWithPopup,
  logout
};

export default auth;
