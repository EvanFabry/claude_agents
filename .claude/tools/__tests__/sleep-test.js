// Simple sleep script for testing timeouts
const sleepMs = parseInt(process.argv[2] || '60000', 10);
const start = Date.now();
while (Date.now() - start < sleepMs) {
  // Busy wait
}
console.log('Done sleeping');
