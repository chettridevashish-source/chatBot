import assert from "node:assert/strict";
import test from "node:test";

import config from "../src/configs/config.js";

test("backend configuration exposes valid local defaults", () => {
    assert.equal(typeof config.port, "number");
    assert.ok(config.port > 0);
    assert.match(config.ragApiUrl, /^https?:\/\//);
    assert.ok(config.clientOrigins.length > 0);
    assert.ok(config.clientOrigins.every((origin) => /^https?:\/\//.test(origin)));
    assert.equal(config.autoStartRag, false);
});
