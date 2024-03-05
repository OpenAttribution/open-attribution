export const csr = false;

import { PUBLIC_DOCS_HOST } from '$env/static/public';

async function fetchContent(page) {
	let htmlContent;
	if (page) {
		// Ensure the path correctly points to where your HTML files are located.
		var mypath = `${PUBLIC_DOCS_HOST}${page.pathname}index.html`;
		console.log(`LETS GO ${mypath}`);
		const response = await fetch(mypath);
		if (response.ok) {
			htmlContent = await response.text();
		} else {
			htmlContent = 'Page not found.';
		}
	}
	htmlContent = `${htmlContent}`;
	// console.log(`GOT CONTENT: ${htmlContent}`)
	return htmlContent;
}

export async function load({ url }) {
	const myhtml = await fetchContent(url);
	return {
		props: {
			mydocs: myhtml
		}
	};
}
