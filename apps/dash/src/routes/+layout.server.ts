import type { PageServerLoad } from './$types';
import { PUBLIC_SUPERSET_INSIDE_DOCKER_HOST } from '$env/static/public';

export const ssr = true;
export const csr = false;

export const load: PageServerLoad = async () => {
	const loginUrl = `http://${PUBLIC_SUPERSET_INSIDE_DOCKER_HOST}:8088/login/`;
	const embedUrl = `http://${PUBLIC_SUPERSET_INSIDE_DOCKER_HOST}:8088/api/v1/dashboard/1/embedded`;

	try {
		const formData = new FormData();
		formData.append('username', 'admin');
		formData.append('password', 'admin');
		// Step 1: POST to login for cookies
		const loginResponse = await fetch(loginUrl, {
			method: 'POST',
			redirect: 'manual',
			headers: {
				Connection: 'keep-alive',
				Accept: '*/*'
			},
			body: formData
		});

		const cookies = loginResponse.headers.get('Set-Cookie');
		if (!cookies) {
			throw new Error('No cookies received');
		}
		const cookieValue = cookies.split(';')[0];

		// Step 2: Get Dash ID
		const dashboardResponse = await fetch(embedUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Cookie: cookieValue
			},
			body: JSON.stringify({ allowed_domains: [] })
		});
		if (!dashboardResponse.ok) {
			throw new Error(`Failed to fetch dashboard ID: ${dashboardResponse.status}`);
		}
		const dashboardData = await dashboardResponse.json();
		const dashboardID = dashboardData?.result?.uuid;
		console.log(`EMBEDDED DASHBOARD: DASHID= ${dashboardID}`);
		return { dashboardID: dashboardID };
	} catch (error) {
		console.error(error);
		return { error: error };
	}
};
