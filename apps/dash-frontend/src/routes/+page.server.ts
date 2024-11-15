import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({
	parent,
	url,
	depends
}) => {

	const startDate = url.searchParams.get('start');
	const endDate = url.searchParams.get('end');

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
