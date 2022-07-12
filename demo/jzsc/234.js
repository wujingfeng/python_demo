
const CryptoJS = require('crypto-js');

function ht(t) {
    return CryptoJS.enc.Hex.parse(t)
}