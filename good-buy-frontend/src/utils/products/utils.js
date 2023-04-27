import axios from "axios";

export const handleFilter = (filter, filters, setState) => {
	const existingFilterIndex = filters.findIndex((f) => f.key === filter.key);

	if (existingFilterIndex !== -1) {
		// If a filter with the same key already exists, remove it from the list or update its values
		const existingFilter = filters[existingFilterIndex];
		if (existingFilter.key === "reverse") {
			const updatedFilter = { ...existingFilter, value: filter.value };
			const updatedFilters = [...filters];
			updatedFilters[existingFilterIndex] = updatedFilter;
			setState((prevState) => ({ ...prevState, filters: updatedFilters }));
		} else {
			const updatedValues = filter.values || [filter.value];
			const newValues = existingFilter.value.includes(filter.value)
				? existingFilter.value.filter((v) => v !== filter.value)
				: [...existingFilter.value, ...updatedValues];
			if (newValues.length) {
				const updatedFilter = { ...existingFilter, value: newValues };
				const updatedFilters = [...filters];
				updatedFilters[existingFilterIndex] = updatedFilter;
				setState((prevState) => ({ ...prevState, filters: updatedFilters }));
			} else {
				const updatedFilters = filters.filter((f, index) => index !== existingFilterIndex);
				setState((prevState) => ({ ...prevState, filters: updatedFilters }));
			}
		}
	} else {
		// If the filter doesn't exist yet, add it to the list with all its values
		const allValues = filter.values || [filter.value];
		const newFilter = { key: filter.key, value: allValues };
		setState((prevState) => ({ ...prevState, filters: [...prevState.filters, newFilter] }));
	}
};

export const filterProducts = async (filters, state, setState, lastSearchTerm) => {
	const filterPairs = {};

	// Use lastSearchTerm from state to build filterPairs object
	if (lastSearchTerm !== "") {
		filterPairs.productName = lastSearchTerm;
	}

	// Build filterPairs object from filters array
	filters.forEach(filter => {
		if (Array.isArray(filter.value)) {
			filterPairs[filter.key] = filter.value.join(",");
		} else {
			filterPairs[filter.key] = filter.value;
		}
	});

	console.log(filterPairs)

	try {
		const productsDataResponse = await axios.get(
			"https://" +
			process.env.REACT_APP_REST_API_ID +
			".execute-api.us-east-1.amazonaws.com/Development/store-apis/filter-products",
			{ params: filterPairs }
		);

		setState(prevState => ({
			...prevState,
			productNotFound: productsDataResponse.data.length === 0,
			productsData: productsDataResponse.data,
			infoLoaded: true
		}));

		return {
			productNotFound: productsDataResponse.data.length === 0,
			productsData: productsDataResponse.data,
			infoLoaded: true
		};
	} catch (error) {
		console.log(error);
		return { productNotFound: true, productsData: [], infoLoaded: true };
	}
};

export const handleChange = (event, value, setState, componentRef) => {
	setState((prevState) => ({ ...prevState, page: value }));
	componentRef.current.scrollIntoView({ behavior: "smooth" });
};

export const handleClick = (event, setAnchorEl) => {
	if (event) {
		event.preventDefault();
		setAnchorEl(event.currentTarget);
	}
};

export const handleClose = (event, setAnchorEl) => {
	if (event) {
		event.preventDefault();
		setAnchorEl(null);
	}
};