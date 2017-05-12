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

    for (let i = 0, len = ALPHABET.length - k, cnt = r; i < len; ++i, ++cnt) {
        TABLE[ALPHABET[i]] = new BitPack(e, cnt);
        // console.log(ALPHABET[i], TABLE[ALPHABET[i]].toString());
    }
    for (let j = ALPHABET.length - k, len = ALPHABET.length, cnt = 0; j < len; ++j, ++cnt) {
        TABLE[ALPHABET[j]] = new BitPack(e + 1, cnt);
        // console.log(ALPHABET[j], TABLE[ALPHABET[j]].toString());
    }
})();

class Tree {
    private UPDATE_TABLE: { [id: string]: TreeNode };
    private NYT: TreeNode;

    private root: TreeNode;

    constructor() {
        this.root = new TreeNode();
        this.NYT = this.root;
        this.UPDATE_TABLE['NTY'] = this.NYT;
    }

    toString(): string {
        let res = '';

        function addNode(node: TreeNode, lv = 0) {
            if (!node) {
                return;
            }

            let prefix = '';
            if (lv > 0) {
                for (let i = 0; i < lv; ++i) {
                    prefix += '    ';
                }
            }

            res += prefix + node.toString() + '\n';
            addNode(node.left, lv + 1);
            addNode(node.right, lv + 1);
        }

        addNode(this.root);
        return res;
    }
}

class TreeNode {
    public parent: TreeNode;
    public left: TreeNode;
    public right: TreeNode;

    toString(): string {

    }
}