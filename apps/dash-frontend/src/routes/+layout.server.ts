import type { LayoutServerLoad } from './$types';

async function fetchData(url: string) {
	try {
		const resp = await fetch(url);
		if (resp.status === 200) {
			return await resp.json();
		} else if (resp.status === 404) {
			console.log('Not found');
			return { error: 'Not Found' };
		} else if (resp.status === 500) {
			console.log('API Server error');
			return { error: 'Backend Error' };
		}
	} catch (error) {
		console.log('Uncaught error', error);
		return { error: 'Uncaught Error' };
	}
}

export const load: LayoutServerLoad = async ({}) => {
	const [respApps, respNets] = await Promise.all([
		fetchData('http://dash-backend:8001/api/apps'),
		fetchData('http://dash-backend:8001/api/networks')
	]);

	return {
		respApps: respApps.error ? { error: respApps.error } : respApps,
		respNets: respNets.error ? { error: respNets.error } : respNets
	};
};
