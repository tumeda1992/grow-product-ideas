import assert from 'node:assert/strict';

class Inventory {
  constructor(members) { this.members = new Set(members); this.items = new Map(); this.events = new Map(); }
  create(actor, id, count = 0) {
    if (!this.members.has(actor)) throw Error('FORBIDDEN');
    if (this.items.size >= 50) throw Error('LIMIT_REACHED');
    this.items.set(id, { count, version: 0 });
  }
  adjust(actor, id, delta, requestId) {
    if (!this.members.has(actor)) throw Error('FORBIDDEN');
    if (![-1, 1].includes(delta)) throw Error('BAD_DELTA');
    const prior = this.events.get(requestId);
    if (prior) {
      if (prior.actor !== actor || prior.id !== id || prior.delta !== delta) throw Error('REQUEST_ID_CONFLICT');
      return prior.after;
    }
    const item = this.items.get(id);
    if (!item) throw Error('NOT_FOUND');
    const after = item.count + delta;
    if (after < 0 || after > 999) throw Error('COUNT_OUT_OF_RANGE');
    item.count = after; item.version += 1;
    this.events.set(requestId, { actor, id, delta, after });
    return after;
  }
}

let passed = 0;
const test = (name, fn) => { fn(); passed++; console.log(`ok ${passed} - ${name}`); };
const inv = new Inventory(['A', 'B']);
inv.create('A', 'milk', 2);
test('A decrements stale value 2 to 1', () => assert.equal(inv.adjust('A', 'milk', -1, 'r1'), 1));
test('B increments from its stale view and final is 2', () => assert.equal(inv.adjust('B', 'milk', 1, 'r2'), 2));
test('both events are retained', () => assert.equal(inv.events.size, 2));
test('same request is idempotent', () => { assert.equal(inv.adjust('B', 'milk', 1, 'r2'), 2); assert.equal(inv.events.size, 2); });
test('request id cannot be reused for another operation', () => assert.throws(() => inv.adjust('A', 'milk', 1, 'r1'), /REQUEST_ID_CONFLICT/));
const empty = new Inventory(['A']); empty.create('A', 'egg', 0);
test('count cannot go below zero', () => assert.throws(() => empty.adjust('A', 'egg', -1, 'r3'), /COUNT_OUT_OF_RANGE/));
test('non-member cannot read through mutation contract', () => assert.throws(() => inv.adjust('X', 'milk', 1, 'r4'), /FORBIDDEN/));
test('50 items allowed and 51st rejected', () => { const x = new Inventory(['A']); for (let i=0;i<50;i++) x.create('A', `i${i}`); assert.throws(() => x.create('A', 'overflow'), /LIMIT_REACHED/); });
console.log(`1..${passed}`);
