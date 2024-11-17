import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ parent, url, depends }) => {
	const startDate = url.searchParams.get('start');
	const endDate = url.searchParams.get('end');

	if (!startDate || !endDate) {
		console.log('No start or end date, setting default');
		const today = new Date();
		const oneWeekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
		const defaultStart = oneWeekAgo.toISOString().split('T')[0];
		const defaultEnd = today.toISOString().split('T')[0];

		// Build the new URL with default query parameters
		const newSearchParams = new URLSearchParams(url.searchParams);
		if (!startDate) newSearchParams.set('start', defaultStart);
		if (!endDate) newSearchParams.set('end', defaultEnd);

		throw redirect(302, `${url.pathname}?${newSearchParams.toString()}`);
	}

	const respData = await fetch(
		`http://dash-backend:8001/api/overview?start_date=${startDate}&end_date=${endDate}`
	);

	depends('app:dates');

	const { respApps, respNets } = await parent();

	return {
		respData: await respData.json(),
		respNets,
		respApps
	};
};
