import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({}) => {
	const [respApps, respNets, clientDomains] = await Promise.all([
		fetch(`http://dash-backend:8001/api/apps`).then((res) => res.json()),
		fetch(`http://dash-backend:8001/api/networks`).then((res) => res.json()),
		fetch(`http://dash-backend:8001/api/links/domains`).then((res) => res.json())
	]);

	console.log(`root layout load apps, networks end`);

	return {
		respApps,
		respNets,
		clientDomains
	};
};
