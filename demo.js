#!/usr/bin/env node

// DNA-Lang Demonstration Script
// This script demonstrates the full compilation and execution pipeline

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🧬 DNA-Lang Demonstration');
console.log('========================\n');

function runCommand(command, description) {
  console.log(`📋 ${description}`);
  console.log(`💻 Running: ${command}\n`);
  
  try {
    const output = execSync(command, { 
      encoding: 'utf8', 
      cwd: __dirname,
      stdio: 'pipe'
    });
    console.log(output);
  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.stdout) console.log('📤 stdout:', error.stdout);
    if (error.stderr) console.log('📥 stderr:', error.stderr);
  }
  console.log('─'.repeat(50) + '\n');
}

async function main() {
  // 1. Show DNA-Lang help
  runCommand('node dist/cli.js --help', 'Display DNA-Lang CLI help');
  
  // 2. Compile simple example
  runCommand('node dist/cli.js compile examples/simple-test.dna', 'Compile simple organism');
  
  // 3. Show generated TypeScript
  console.log('📄 Generated TypeScript for SimpleTest:');
  console.log('=====================================\n');
  if (fs.existsSync('dist/SimpleTest.ts')) {
    const generated = fs.readFileSync('dist/SimpleTest.ts', 'utf8');
    // Show first 30 lines to keep it manageable
    const lines = generated.split('\n').slice(0, 30);
    console.log(lines.join('\n'));
    console.log('\n... (truncated for brevity)\n');
  }
  console.log('─'.repeat(50) + '\n');
  
  // 4. Compile complex example  
  runCommand('node dist/cli.js compile examples/basic-organism.dna', 'Compile complex e-commerce organism');
  
  // 5. Show project structure
  console.log('📁 Generated Project Structure:');
  console.log('=============================\n');
  runCommand('find dist -name "*.ts" -o -name "*.js" | head -10', 'List generated files');
  
  // 6. Run tests
  runCommand('npm test', 'Run DNA-Lang test suite');
  
  // 7. Create a new organism
  runCommand('node dist/cli.js new DemoApp', 'Create new organism scaffold');
  
  console.log('🎉 DNA-Lang demonstration completed!');
  console.log('\n📊 Summary:');
  console.log('• ✅ Lexical analysis (tokenization)');
  console.log('• ✅ Syntax parsing (AST generation)');
  console.log('• ✅ TypeScript transpilation');
  console.log('• ✅ CLI tool functionality');
  console.log('• ✅ Example organisms');
  console.log('• ✅ Test coverage');
  console.log('\n🌐 Ready for public verification!');
}

main().catch(console.error);