import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({}) => {
	const [respApps, respNets] = await Promise.all([
		fetch(`http://dash-backend:8001/api/apps`).then((res) => res.json()),
		fetch(`http://dash-backend:8001/api/networks`).then((res) => res.json())
	]);

	console.log(`root layout load apps, networks end`);

	return {
		respApps: respApps,
		respNets: respNets
	};
};
