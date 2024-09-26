import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ params }) => {
	const id = 1;

	return {
		myapp: fetch(`http://dash-backend:8001/api/overview?start_date=2024-12-12&end_date=2024-12-12`)
			.then((resp) => {
				if (resp.status === 200) {
					return resp.json();
				} else if (resp.status === 404) {
					console.log('App Not found');
					return 'App Not Found';
				} else if (resp.status === 500) {
					console.log('App API Server error');
					return 'Backend Error';
				}
			})
			.then(
				(json) => json,
				(error) => {
					console.log('Uncaught error', error);
					return 'Uncaught Error';
				}
			)
	};
};
