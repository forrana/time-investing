module.exports = {
  "moduleFileExtensions": [
      "ts",
      "tsx",
      "js",
      "jsx",
      "json",
      "node"
  ],
  "roots": [
    "./src"
  ],
  // Setup Enzyme
  "setupTestFrameworkScriptFile": "./src/setupTests.ts",
  "snapshotSerializers": ["enzyme-to-json/serializer"],
  "testRegex": "(/__tests__/.*|(\\.|/)(test|spec))\\.tsx?$",
  "transform": {
    "^.+\\.tsx?$": "ts-jest"
  },
};
