export const ssr = true;
export const csr = true;

import { PUBLIC_SUPERSET_HOST_NAME } from '$env/static/public';

export async function load() {
	// Define the URL where you want to send the POST request
	const loginurl = `http://${PUBLIC_SUPERSET_HOST_NAME}:8088/api/v1/security/login`;

	// Define the payload
	const loginpayload = {
		password: 'admin',
		// "password":"loginpass",
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
		throw new Error(`Login failed: ${PUBLIC_SUPERSET_HOST_NAME}:8088`);
	}
	// Extract the access token from the login response
	const loginData = await loginResponse.json();
	const myAccessToken = loginData.access_token; // Assuming the token is in the 'access_token' field

	const url = `http://${PUBLIC_SUPERSET_HOST_NAME}:8088/api/v1/security/guest_token`;

	// Define the payload
	const payload = {
		user: {
			username: 'myuser',
			first_name: 'Stan',
			last_name: 'Lee'
		},
		resources: [
			{
				type: 'dashboard',
				// id: 'd7012462-5f39-48f1-96b4-fee1d7b2b3ac'
				id: '47d4d3a7-c2b0-46c5-80ad-dc7ee0e68ef9'
			}
		],
		rls: []
	};

	console.info(`Inside request: accessToken ${myAccessToken}`);

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
		// You can add more error handling logic here, like throwing the error
		throw error;
	}

	// Parse the response (assuming it's JSON)
	const data = await response.json();

	// Return the data or do something with it
	return {
		props: { data }
	};
}
