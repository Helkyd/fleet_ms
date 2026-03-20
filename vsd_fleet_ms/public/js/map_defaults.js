// Make sure we have a dictionary to add our custom settings
const map_settings = frappe.provide("frappe.utils.map_defaults");

// Center and zoomlevel can be copied from the URL of
// the map view at openstreetmap.org.

// New default location ANGOLA.
// Angola is located at latitude -11.202692 and longitude 17.873887
map_settings.center = [-11.202692, 17.873887];
// new zoomlevel: see the whole country, not just a single city
map_settings.zoom = 5.5;

// Use a different map: satellite instead of streets
// Examples can be found at https://leaflet-extras.github.io/leaflet-providers/preview/
//map_settings.tiles =
//	"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
map_settings.tiles = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
//map_settings.attribution =
//	"Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community";

//map_settings.attribution = 'OSM'
map_settings.attribution = 'OSM; &#169; <a href="//www.openstreetmap.org/">OpenStreetMap</a> contributors, CC BY-SA license';