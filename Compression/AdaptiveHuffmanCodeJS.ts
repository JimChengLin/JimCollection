const ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~';
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

    fromString(str: string) {

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
        console.log(ALPHABET[i], TABLE[ALPHABET[i]].toString());
    }
    for (let j = ALPHABET.length - k, len = ALPHABET.length, cnt = 0; j < len; ++j, ++cnt) {
        TABLE[ALPHABET[j]] = new BitPack(e + 1, cnt);
        console.log(ALPHABET[j], TABLE[ALPHABET[j]].toString());
    }
})();

class Tree {
    private UPDATE_TABLE: { [id: string]: TreeNode };
    private NYT: TreeNode;

    private root: TreeNode;

    constructor() {
        this.UPDATE_TABLE = {};
        this.root = new TreeNode();
        this.NYT = this.root;
        this.NYT.char = 'NYT';
        this.UPDATE_TABLE['NTY'] = this.NYT;
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
            this.increaseWeight(charNode);
        }

        return res;
    }

    private addChar(char: string) {
        let NYTParent = new TreeNode();
        let newCharNode = new TreeNode();

        if (this.NYT.parent) {
            this.NYT.parent.bindLeft(NYTParent);
        } else {
            this.root = NYTParent;
        }

        NYTParent.bindLeft(this.NYT);
        NYTParent.bindRight(newCharNode);
        ++NYTParent.weight;

        newCharNode.char = char;
        this.increaseWeight(newCharNode);
        this.UPDATE_TABLE[char] = newCharNode;
    }

    private increaseWeight(node: TreeNode) {
        ++node.weight;
        this.tryMoveUp(node, node.parent);
    }

    private tryMoveUp(node: TreeNode, target: TreeNode) {
        if (target == this.root && target.right.weight >= node.weight) {
            target.updateWeight();
            return;
        }

        // 优先向上
        if (target.weight < node.weight) {
            // 递归
            if (target.parent && target.parent.weight < node.weight) {
                return this.tryMoveUp(node, target.parent);
            }

            this.swapNode(node, target);
        } else if (target.right.weight < node.weight) {
            this.swapNode(node, target.right);
        }

        node.parent.updateWeight();
        if (node.parent.parent) {
            this.tryMoveUp(node.parent, node.parent.parent);
        }
    }

    private swapNode(a: TreeNode, b: TreeNode) {
        if (a.parent == b.parent) {
            [a.parent.left, a.parent.right] = [a.parent.right, a.parent.left];
            return;
        }

        if (a.parent.left == a) {
            a.parent.bindLeft(b);
        } else {
            a.parent.bindRight(b);
        }
        if (b.parent.left == b) {
            b.parent.bindLeft(a);
        } else {
            b.parent.bindRight(a);
        }

        if (b == this.root) {
            this.root = a;
        }
    }
}

class TreeNode {
    parent: TreeNode;
    left: TreeNode;
    right: TreeNode;

    char: string;
    weight = 0;

    toString(): string {
        if (this.char) {
            return this.char + ' ' + this.weight.toString();
        } else {
            return '+ ' + this.weight.toString();
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

    updateWeight() {
        this.weight = 0;
        if (this.left) {
            this.weight += this.left.weight;
        }
        if (this.right) {
            this.weight += this.right.weight;
        }
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

        console.log('Out: ', char, res.toString(), TABLE[char].toString());
        console.log(tree.toString());
    }

    let str = holder.toString();
    console.log(str);
})();
