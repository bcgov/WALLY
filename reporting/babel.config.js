module.exports = function (api) {
    api.cache(true);

    const presets = [
        [
            "@babel/env",
            {
                targets: {
                    edge: "17",
                    firefox: "60",
                    chrome: "67",
                    safari: "11.1",
                },
                useBuiltIns: "usage",
            },
        ],
        ["@babel/react"]
    ]

    const plugins = [
        [
            "file-loader",
            {
                "name": "[hash].[ext]",
                "extensions": ["png", "jpg", "jpeg", "gif", "svg", "ttf"],
                "publicPath": __dirname + "/build/src/assets",
                "outputPath": "build/src/assets",
                "context": "",
                "limit": 0
            }
        ]
    ]

    return {
        presets,
        plugins
    };
}
