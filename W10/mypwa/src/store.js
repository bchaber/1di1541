import { writable } from "svelte/store";

export const authenticated = writable(false);
export const authorized = writable(false);
export const popup = writable(false);
export const user = writable({});
export const token = writable();
export const error = writable();

export const tasks = writable([]);