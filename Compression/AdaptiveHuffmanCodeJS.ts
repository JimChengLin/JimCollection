const ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~' + `:/?#[]@!$&'()*+,;=`;
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

    extend(other: BitPack): BitPack {
        this.len += other.len;
        this.val <<= other.len;
        this.val |= other.val;
        return this;
    }
}

class BitPackHolder {
    container: BitPack[];

    constructor() {
        this.container = [];
    }

    toString(): string {
        return this.bitArray().join('');
    }

    private *bitStream(): Iterable<number> {
        for (let i = this.container.length - 1; i >= 0; --i) {
            let bitPack = this.container[i];
            for (let j = 0, len = bitPack.len; j < len; ++j) {
                yield +Boolean(bitPack.val & (1 << j));
            }
        }
    }

    private bitArray(): number[] {
        let bitArray: number[] = [];
        for (let bit of this.bitStream()) {
            bitArray.push(bit);
        }
        return bitArray.reverse();
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
        this.NYT.char = 'NYT';
        this.UPDATE_TABLE = {'NYT': this.NYT};
    }

    toString(): string {
        let res = '';

        function add(node: TreeNode, lv = 0) {
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
            add(node.left, lv + 1);
            add(node.right, lv + 1);
        }

        add(this.root);
        return res;
    }

    encode(char: string): BitPack {
        let res: BitPack;

        if (!this.UPDATE_TABLE.hasOwnProperty(char)) {
            res = this.NYT.toBitPack().extend(TABLE[char]);
            this.addChar(char);
        } else {
            let charNode = this.UPDATE_TABLE[char];
            res = charNode.toBitPack();
            this.tryMoveThenIncrease(charNode);
        }

        return res;
    }

    private addChar(char: string) {
        const NYTParent = new TreeNode();
        const charNode = new TreeNode();

        if (this.NYT.parent) {
            this.NYT.parent.bindLeft(NYTParent);
        } else {
            this.root = NYTParent;
        }

        NYTParent.bindLeft(this.NYT);
        NYTParent.bindRight(charNode);
        ++NYTParent.weight;

        charNode.char = char;
        this.UPDATE_TABLE[char] = charNode;
        ++charNode.weight;

        this.tryMoveThenIncrease(NYTParent.parent);
    }

    private tryMoveThenIncrease(node: TreeNode) {
        if (!node) {
            return;
        } else if (node == this.root) {
            ++node.weight;
            return;
        }

    }
}

class TreeNode {
    parent?: TreeNode;
    left?: TreeNode;
    right?: TreeNode;

    char?: string;
    weight = 0;

    toString(): string {
        if (this.char) {
            return this.char + ' ' + this.weight.toString();
        } else {
            return '- ' + this.weight.toString();
        }
    }

    toBitPack(): BitPack {
        let cnt = 0;
        let code = 0;
        let cursor: TreeNode = this;
        while (cursor.parent) {
            ++cnt;
            code <<= 1;

            if (cursor == cursor.parent.right) {
                code |= 1;
            }
            cursor = cursor.parent;
        }
        return new BitPack(cnt, code);
    }

    bindLeft(node: TreeNode) {
        this.left = node;
        node.parent = this;
    }

    bindRight(node: TreeNode) {
        this.right = node;
        node.parent = this;
    }
}

(function main() {
    let tree = new Tree();
    let holder = new BitPackHolder();

    for (let char of 'aardv') {
        let res = tree.encode(char);
        holder.container.push(res);

        console.log('out: ', char, res.toString(), TABLE[char].toString());
        console.log(tree.toString());
    }

    console.log(holder.toString());
})();
