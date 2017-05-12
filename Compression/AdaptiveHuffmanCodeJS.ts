const ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~';
const TABLE: { [id: string]: BitPack } = {};

class BitPack {
    constructor(public len: number, public val: number) {
    }

    toString(): string {
        let res = '0b';
        const binVal = this.val.toString(2);
        for (let i = 0, len = this.len - binVal.length; i < len; ++i) {
            res += '0';
        }
        res += binVal;
        return res;
    }

    merge(other: BitPack): BitPack {
        this.len += other.len;
        this.val <<= other.len;
        this.val |= other.val;
        return this;
    }
}

(function init() {
    const e = Math.floor(Math.log2(ALPHABET.length));
    const r = ALPHABET.length - Math.pow(2, e);
    const k = 2 * r;

    let i = 0;
    for (let len = ALPHABET.length - k, cnt = r; i < len; ++i, ++cnt) {
        TABLE[ALPHABET[i]] = new BitPack(e, cnt);
        // console.log(ALPHABET[i], TABLE[ALPHABET[i]].toString());
    }
    for (let j = i, len = j + k, cnt = 0; j < len; ++j, ++cnt) {
        TABLE[ALPHABET[j]] = new BitPack(e + 1, cnt);
        // console.log(ALPHABET[j], TABLE[ALPHABET[j]].toString());
    }
})();

class Tree {
    private UPDATE_TABLE: { [id: string]: TreeNode };
    private NYT: TreeNode;

    private root: TreeNode;

    constructor() {
    }
}

class TreeNode {

}