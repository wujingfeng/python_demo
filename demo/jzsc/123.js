const CryptoJS = require('crypto-js');


f = CryptoJS.enc.Utf8.parse("jo8j9wGw%6HbxfFn")
m = CryptoJS.enc.Utf8.parse("0123456789ABCDEF")

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
