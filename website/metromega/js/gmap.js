var map;
$(window).load(function() {
    map = new GMaps({
        div: '#gmap',
        lat: 37.776715,
        lng: -122.416998
    });

    map.addMarker({
        lat: 37.776715,
        lng: -122.416998,
        title: 'Twitter Inc.'
    });

});