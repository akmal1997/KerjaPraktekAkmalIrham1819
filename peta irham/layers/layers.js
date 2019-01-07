var wms_layers = [];
var lyr_S07E105_0 = new ol.layer.Image({
                            opacity: 1,
                            title: "S07E105",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S07E105_0.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11688500.150173, -781228.945659, 11799912.407208, -669094.418450]
                            })
                        });var lyr_S06E106_1 = new ol.layer.Image({
                            opacity: 1,
                            title: "S06E106",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S06E106_1.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11799819.640966, -669187.695674, 11911231.898001, -557258.696992]
                            })
                        });var lyr_S06E107_2 = new ol.layer.Image({
                            opacity: 1,
                            title: "S06E107",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S06E107_2.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11911139.131759, -669187.695674, 12022551.388795, -557258.696992]
                            })
                        });var lyr_S07E106_3 = new ol.layer.Image({
                            opacity: 1,
                            title: "S07E106",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S07E106_3.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11799819.640966, -781228.945659, 11911231.898001, -669094.418450]
                            })
                        });var lyr_S07E107_4 = new ol.layer.Image({
                            opacity: 1,
                            title: "S07E107",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S07E107_4.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11911139.131759, -781228.945659, 12022551.388795, -669094.418450]
                            })
                        });var lyr_S08E106_5 = new ol.layer.Image({
                            opacity: 1,
                            title: "S08E106",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S08E106_5.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11799819.640966, -893510.589991, 11911231.898001, -781135.482759]
                            })
                        });var lyr_S08E107_6 = new ol.layer.Image({
                            opacity: 1,
                            title: "S08E107",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S08E107_6.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11911139.131759, -893510.589991, 12022551.388795, -781135.482759]
                            })
                        });var lyr_S06E105_7 = new ol.layer.Image({
                            opacity: 1,
                            title: "S06E105",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S06E105_7.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11688500.150173, -669187.695674, 11799912.407208, -557258.696992]
                            })
                        });var lyr_S08E105_8 = new ol.layer.Image({
                            opacity: 1,
                            title: "S08E105",
                            
                            
                            source: new ol.source.ImageStatic({
                               url: "./layers/S08E105_8.png",
    attributions: '<a href=""></a>',
                                projection: 'EPSG:3857',
                                alwaysInRange: true,
                                imageExtent: [11688500.150173, -893510.589991, 11799912.407208, -781135.482759]
                            })
                        });
        var lyr_terrains_9 = new ol.layer.Tile({
            'title': 'terrains_9',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: '<a href=""></a>',
                url: 'http://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}'
            })
        });

lyr_S07E105_0.setVisible(true);lyr_S06E106_1.setVisible(true);lyr_S06E107_2.setVisible(true);lyr_S07E106_3.setVisible(true);lyr_S07E107_4.setVisible(true);lyr_S08E106_5.setVisible(true);lyr_S08E107_6.setVisible(true);lyr_S06E105_7.setVisible(true);lyr_S08E105_8.setVisible(true);lyr_terrains_9.setVisible(true);
var layersList = [lyr_S07E105_0,lyr_S06E106_1,lyr_S06E107_2,lyr_S07E106_3,lyr_S07E107_4,lyr_S08E106_5,lyr_S08E107_6,lyr_S06E105_7,lyr_S08E105_8,lyr_terrains_9];
