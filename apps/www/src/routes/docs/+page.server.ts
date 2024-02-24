// Assuming you're fetching static HTML content based on a route parameter.
async function fetchContent(page) {
	let htmlContent;
	if (page) {
		// Construct the URL dynamically based on the page parameter.
		// Ensure the path correctly points to where your HTML files are located.
		const response = await fetch(`localhost:5173/static/docs/${page.pathname}/index.html`);
		if (response.ok) {
			htmlContent = await response.text();
		} else {
			htmlContent = 'Page not found.';
		}
	}
	return htmlContent;
}

export async function load({ url }) {
	// Use params.page to get the dynamic part of the route, assuming your file structure matches your URL structure.
	// e.g., for a URL like `/docs/about`, params.page would be `about`.
	const myhtml = await fetchContent(url);

	// Return the fetched HTML content as a prop to the component.
	return {
		props: {
			myhtml: myhtml
		}
	};
}
