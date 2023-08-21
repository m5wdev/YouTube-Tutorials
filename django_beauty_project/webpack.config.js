const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const { VueLoaderPlugin } = require('vue-loader');


module.exports = {
    mode: 'production',
    // mode: 'development',

    // entry: './layout/src/main.js',
    entry: {
        main: './layout/src/main.js',
        '2Gis': './layout/src/js/2gis.js',
        'search_filters': './layout/src/js/search_filters.js'
    },
    output: {
        filename: 'js/[name].js',
        path: path.resolve(__dirname, './layout/dist'),
        publicPath: '../'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.(png|svg|jpe?g|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'images/',
                            useRelativePath: true
                        }
                    },
                    {
                        loader: 'image-webpack-loader',
                        options: {
                            mozjpeg: {
                                progressive: true,
                                quality: 70
                            },
                            optipng: {
                                enabled: true,
                            },
                            pngquant: {
                                quality: [0.65, 0.90],
                                speed: 4
                            }
                        }
                    }
                ]
            },

            {
                test: /.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    'vue-style-loader',
                    'css-loader'
                ]
            },
            // Fonts loader
            // {
            //     test: /\.(woff(2)?|ttf|eot)(\?v=\d+\.\d+\.\d+)?$/,
            //     use: [
            //         {
            //             loader: 'file-loader',
            //             options: {
            //                 name: '[name].[ext]',
            //                 outputPath: 'fonts/'
            //             }
            //         }
            //     ]
            // },
        ]
    },
    optimization: {
        splitChunks: {
            chunks: 'all'
        }
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
    },
    plugins: [
        // Clean
        // new CleanWebpackPlugin(),

        // Vue
        new VueLoaderPlugin(),

        // Copy
        new CopyWebpackPlugin({
            patterns: [
                {
                    from: './layout/src/images/favicons',
                    to: 'images/favicons'
                },
                {
                    from: './layout/src/images/tmp',
                    to: 'images/tmp'
                },
            ],
        }),

        // Add jQuery to Webpack
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            Popper: ['popper.js', 'default'],
        }),

        new MiniCssExtractPlugin({
            filename: 'css/styles.css'
        }),

        new OptimizeCssAssetsPlugin({
            // CSS minification
            assetNameRegExp: /\.css$/g,
            cssProcessor: require('cssnano'),
            cssProcessorPluginOptions: {
                preset: ['default', {
                    discardComments: {
                        removeAll: true
                    }
                }]
            },
            canPrint: true
        }),

        new HtmlWebpackPlugin({
            filename: 'html/homepage.html',
            template: './layout/src/html/homepage.html',
            // chunks: ["main", "2Gis", "search_filters"]
            chunks: ["main", "2Gis"]
        }),

        // ...
        // new HtmlWebpackPlugin({
        //     filename: 'html/products_list.html',
        //     template: './layout/src/html/shop/products_list.html'
        // }),
    ]
}
