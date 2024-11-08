import type { PageServerLoad, PageServerParentData } from './$types';

export const load: PageServerLoad = async ({
	parent,
	url
}: {
	parent: () => Promise<PageServerParentData>;
	url: URL;
}) => {
	const startDate = url.searchParams.get('start');
	const endDate = url.searchParams.get('end');
	const { respApps, respNets } = await parent();

	return {
		respData: await fetch(
			`http://dash-backend:8001/api/overview?start_date=${startDate}&end_date=${endDate}`
		)
			.then((resp) => {
				console.log('/api/overview: load overview data...');
				if (resp.status === 200) {
					return resp.json();
				} else if (resp.status === 404) {
					console.log('Not found');
					return 'Not Found';
				} else if (resp.status === 500) {
					console.log('API Server error');
					return 'Backend Error';
				}
			})
			.then(
				(json) => json,
				(error) => {
					console.log('Uncaught error', error);
					return 'Uncaught Error';
				}
			),
		respNets,
		respApps
	};
};
