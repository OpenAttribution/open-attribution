export const ssr = true;
// NOTE currently this CSR must be true for superset to run
export const csr = true;

// NOTE: This is only for docker, will need localhost if not in docker
import { PUBLIC_SUPERSET_INSIDE_DOCKER_HOST } from '$env/static/public';

export async function load({ parent }) {
	const { dashboardID } = await parent();

	const loginurl = `http://${PUBLIC_SUPERSET_INSIDE_DOCKER_HOST}:8088/api/v1/security/login`;

	try {
		// Define the payload
		const loginpayload = {
			password: 'admin',
			provider: 'db',
			// "refresh":true,
			username: 'admin'
		};

		// Make the POST request
		const loginResponse = await fetch(loginurl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(loginpayload)
		});

		// Check if the login request was successful
		if (!loginResponse.ok) {
			throw new Error(`Login failed: ${PUBLIC_SUPERSET_INSIDE_DOCKER_HOST}:8088`);
		}
		// Extract the access token from the login response
		const loginData = await loginResponse.json();
		const myAccessToken = loginData.access_token;

		console.info(`GOT accessToken`);

		const url = `http://${PUBLIC_SUPERSET_INSIDE_DOCKER_HOST}:8088/api/v1/security/guest_token`;

		// Define the payload
		const payload = {
			user: {
				username: 'admin', //TODO: @ddxv make embedUser
				first_name: 'Stan',
				last_name: 'Lee'
			},
			resources: [
				{
					type: 'dashboard',
					id: dashboardID
				}
			],
			rls: []
		};

		// Make the POST request
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${myAccessToken}`
			},
			body: JSON.stringify(payload)
		});

		// Check if the request was successful
		if (!response.ok) {
			const text = await response.text();
			const error = new Error(`An error occurred while fetching the data: ${text}`);
			console.error(error);
			throw error;
		}
		console.info(`GOT dashboard data`);

		const data = await response.json();

		return {
			props: { data }
		};
	} catch (error) {
		console.error(error);
		return { error: error };
	}
}
