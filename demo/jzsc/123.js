const CryptoJS = require('crypto-js');


f = CryptoJS.enc.Utf8.parse("jo8j9wGw%6HbxfFn")
m = CryptoJS.enc.Utf8.parse("0123456789ABCDEF")

function ht(t) {
    return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Hex.parse(t))

}
function h(t) {
    var e = CryptoJS.enc.Hex.parse(t)
        // , ce = CryptoJS.enc.Hex.parse(t)
        , n = CryptoJS.enc.Base64.stringify(e)
        , a = CryptoJS.AES.decrypt(n, f, {
        iv: m,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    })
        , r = a.toString(CryptoJS.enc.Utf8);
    console.log(e)
    // console.log(ce)
    return r.toString()
}

function hex_parse(e) {
    for (var t = e.length, n = [], i = 0; i < t; i += 2)
        n[i >>> 3] |= parseInt(e.substr(i, 2), 16) << 24 - i % 8 * 4;
    return s_init(n, t / 2)
}


function base64_stringify(e) {
    var t = e.words
        , n = e.sigBytes
        , i = i;
    e.clamp();
    for (var r = [], o = 0; o < n; o += 3)
        for (var s = t[o >>> 2] >>> 24 - o % 4 * 8 & 255, a = t[o + 1 >>> 2] >>> 24 - (o + 1) % 4 * 8 & 255, l = t[o + 2 >>> 2] >>> 24 - (o + 2) % 4 * 8 & 255, c = s << 16 | a << 8 | l, u = 0; u < 4 && o + .75 * u < n; u++)
            r.push(i.charAt(c >>> 6 * (3 - u) & 63));
    var h = i.charAt(64);
    if (h)
        while (r.length % 4)
            r.push(h);
    return r.join("")
}


function clamp() {
    var t = this.words
        , n = this.sigBytes;
    t[n >>> 2] &= 4294967295 << 32 - n % 4 * 8,
        t.length = Math.ceil(n / 4)
}

function decrypt(e, t, n, i) {
    i = this.cfg.extend(i),
        t = _parse(t, i.format);
    var r = e.createDecryptor(n, i).finalize(t.ciphertext);
    return r
}

function extend(e) {
    var t = n(this);
    return e && t.mixIn(e),
    t.hasOwnProperty("init") && this.init !== t.init || (t.init = function () {
            t.$super.init.apply(this, arguments)
        }
    ),
        t.init.prototype = t,
        t.$super = this,
        t
}

function _parse(e, t) {
    return "string" == typeof e ? t.parse(e, this) : e
}

function init(e, n) {
    return e = this.words = e || [],
        this.sigBytes = n != t ? n : 4 * e.length
}

function s_init(e) {
    if (e instanceof ArrayBuffer && (e = new Uint8Array(e)),
    (e instanceof Int8Array || "undefined" !== typeof Uint8ClampedArray && e instanceof Uint8ClampedArray || e instanceof Int16Array || e instanceof Uint16Array || e instanceof Int32Array || e instanceof Uint32Array || e instanceof Float32Array || e instanceof Float64Array) && (e = new Uint8Array(e.buffer, e.byteOffset, e.byteLength)),
    e instanceof Uint8Array) {
        for (var t = e.byteLength, n = [], i = 0; i < t; i++)
            n[i >>> 2] |= e[i] << 24 - i % 4 * 8;
        return init(n, t)
    } else
        return init(arguments)
}

function aes_decrypt(n, i, r) {
    return e(i).decrypt(t, n, i, r)
}