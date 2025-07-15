#!/usr/bin/env ts-node
import { CharStreams, CommonTokenStream } from 'antlr4ts';
import { dnaorganismLexer } from './parser/grammar/dnaorganismLexer';
import { dnaorganismParser } from './parser/grammar/dnaorganismParser';
import { dnaorganismVisitor } from './parser/grammar/dnaorganismVisitor';
import * as fs from 'fs';

class ASTBuilder extends dnaorganismVisitor<any> {
  visitProgram(ctx: any) {
    return {
      type: 'Program',
      organisms: ctx.organismDef()?.map((o: any) => this.visit(o)) || []
    };
  }
  visitOrganismDef(ctx: any) {
    return {
      type: 'Organism',
      name: ctx.ID().text,
      dna: this.visit(ctx.dnaBlock()),
      genome: this.visit(ctx.genomeBlock()),
      agents: this.visit(ctx.agentsBlock())
    };
  }
  visitDnaBlock(ctx: any) {
    return {
      type: 'DNA',
      attributes: ctx.attrPair()?.map((a: any) => this.visit(a)) || []
    };
  }
  visitGenomeBlock(ctx: any) {
    return {
      type: 'Genome',
      genes: ctx.geneDef()?.map((g: any) => this.visit(g)) || []
    };
  }
  visitGeneDef(ctx: any) {
    return {
      type: 'Gene',
      name: ctx.ID().text,
      body: ctx.geneBody()?.map((b: any) => this.visit(b)) || []
    };
  }
  visitMutationsBlock(ctx: any) {
    return {
      type: 'Mutations',
      mutations: ctx.mutationDef()?.map((m: any) => this.visit(m)) || []
    };
  }
  visitMutationDef(ctx: any) {
    return {
      type: 'Mutation',
      name: ctx.ID().text,
      attributes: ctx.attrPair()?.map((a: any) => this.visit(a)) || []
    };
  }
  visitImmuneBlock(ctx: any) {
    return {
      type: 'ImmuneSystem',
      attributes: ctx.attrPair()?.map((a: any) => this.visit(a)) || []
    };
  }
  visitAdaptiveBlock(ctx: any) {
    return {
      type: 'AdaptiveResponses',
      attributes: ctx.attrPair()?.map((a: any) => this.visit(a)) || []
    };
  }
  visitAgentsBlock(ctx: any) {
    return {
      type: 'Agents',
      assignments: ctx.agentAssign()?.map((a: any) => this.visit(a)) || []
    };
  }
  visitAgentAssign(ctx: any) {
    return {
      agent: ctx.ID(0).text,
      gene: ctx.ID(1).text
    };
  }
  visitAttrPair(ctx: any) {
    const value = ctx.STRING() ? ctx.STRING().text.slice(1, -1) : parseFloat(ctx.NUMBER().text);
    return {
      key: ctx.ID().text,
      value
    };
  }
}

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: dnalang <file.dna>');
    process.exit(1);
  }
  const source = fs.readFileSync(file, 'utf8');
  const inputStream = CharStreams.fromString(source);
  const lexer = new dnaorganismLexer(inputStream);
  const tokenStream = new CommonTokenStream(lexer);
  const parser = new dnaorganismParser(tokenStream);
  const tree = parser.program();
  const visitor = new ASTBuilder();
  const ast = visitor.visit(tree);
  console.log(JSON.stringify(ast, null, 2));
}

if (require.main === module) {
  main();
}