// the map trigger indicates a search was triggered by moving the map.
// this should update the search results table to only show visible wells
export const MAP_TRIGGER = 'MAP_TRIGGER'

// the QUERY trigger means the search was triggered by a querystring in the URL
// e.g. the user bookmarked a search or shared a link.
export const QUERY_TRIGGER = 'QUERY_TRIGGER'

// the search trigger means the basic or advanced search form was used to search for wells.
export const SEARCH_TRIGGER = 'SEARCH_TRIGGER'

// the filter trigger means that the search was triggered via search result filters.
export const FILTER_TRIGGER = 'FILTER_TRIGGER'
