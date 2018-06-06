This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

## Table of Contents

- [Folder Structure](#folder-structure)
- [Available Scripts](#available-scripts)
  - [npm start](#npm-start)
  - [npm test](#npm-test)
- [Displaying Lint Output in the Editor](#displaying-lint-output-in-the-editor)

## Folder Structure

```
dna-app/
  README.md
  node_modules/
  .eslintrc
  package.json
  public/
    index.html
  src/
    App.css
    App.js
    App.test.js
    index.css
    index.js
    ..
    helpers/
      constants.js
      regex.js
      utils.js
      validator.js
```

For the project to build, **these files must exist with exact filenames**:

* `public/index.html` is the page template;
* `src/index.js` is the JavaScript entry point.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](#running-tests) for more information.

## Displaying Lint Output in the Editor

.eslintr is include in the project

```js
{
  "extends": "react-app"
}
```

Now your editor should report the linting warnings.
