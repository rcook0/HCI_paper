const StyleDictionary = require('style-dictionary');
const Handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');
const templatesDir = path.join(__dirname, 'templates');
const tpl = (name) => Handlebars.compile(fs.readFileSync(path.join(templatesDir, name), 'utf8'));

StyleDictionary.registerFormat({
  name: 'custom/winui-xaml',
  formatter: ({ dictionary }) => tpl('winui.hbs')({ tokens: dictionary.allTokens })
});
StyleDictionary.registerFormat({
  name: 'custom/qt-mjs',
  formatter: ({ dictionary }) => tpl('qt.mjs.hbs')({ tokens: dictionary.allTokens })
});
StyleDictionary.registerFormat({
  name: 'custom/gtk-css',
  formatter: ({ dictionary }) => tpl('gtk.css.hbs')({ tokens: dictionary.allTokens })
});

module.exports = {
  source: ['tokens/base/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/css/',
      files: [{ destination: 'themes.css', format: 'css/variables', options: { outputReferences: true, selector: ':root[data-theme="light"]' } }]
    },
    json: {
      transformGroup: 'js',
      buildPath: 'dist/json/',
      files: [{ destination: 'tokens.json', format: 'json' }]
    },
    winui: {
      transformGroup: 'js',
      buildPath: 'dist/winui/',
      files: [{ destination: 'Resources.xaml', format: 'custom/winui-xaml' }]
    },
    qt: {
      transformGroup: 'js',
      buildPath: 'dist/qt/',
      files: [{ destination: 'tokens.mjs', format: 'custom/qt-mjs' }]
    },
    gtk: {
      transformGroup: 'css',
      buildPath: 'dist/gtk/',
      files: [{ destination: 'tokens.css', format: 'custom/gtk-css' }]
    }
  }
};
