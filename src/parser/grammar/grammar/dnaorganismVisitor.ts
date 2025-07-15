// Generated from grammar/dnaorganism.g4 by ANTLR 4.9.0-SNAPSHOT


import { ParseTreeVisitor } from "antlr4ts/tree/ParseTreeVisitor";

import { ProgramContext } from "./dnaorganismParser";
import { OrganismDefContext } from "./dnaorganismParser";
import { DnaBlockContext } from "./dnaorganismParser";
import { GenomeBlockContext } from "./dnaorganismParser";
import { GeneDefContext } from "./dnaorganismParser";
import { GeneBodyContext } from "./dnaorganismParser";
import { MutationsBlockContext } from "./dnaorganismParser";
import { MutationDefContext } from "./dnaorganismParser";
import { ImmuneBlockContext } from "./dnaorganismParser";
import { AdaptiveBlockContext } from "./dnaorganismParser";
import { AgentsBlockContext } from "./dnaorganismParser";
import { AgentAssignContext } from "./dnaorganismParser";
import { AttrPairContext } from "./dnaorganismParser";


/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by `dnaorganismParser`.
 *
 * @param <Result> The return type of the visit operation. Use `void` for
 * operations with no return type.
 */
export interface dnaorganismVisitor<Result> extends ParseTreeVisitor<Result> {
	/**
	 * Visit a parse tree produced by `dnaorganismParser.program`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitProgram?: (ctx: ProgramContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.organismDef`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitOrganismDef?: (ctx: OrganismDefContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.dnaBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitDnaBlock?: (ctx: DnaBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.genomeBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitGenomeBlock?: (ctx: GenomeBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.geneDef`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitGeneDef?: (ctx: GeneDefContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.geneBody`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitGeneBody?: (ctx: GeneBodyContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.mutationsBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitMutationsBlock?: (ctx: MutationsBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.mutationDef`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitMutationDef?: (ctx: MutationDefContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.immuneBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitImmuneBlock?: (ctx: ImmuneBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.adaptiveBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitAdaptiveBlock?: (ctx: AdaptiveBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.agentsBlock`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitAgentsBlock?: (ctx: AgentsBlockContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.agentAssign`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitAgentAssign?: (ctx: AgentAssignContext) => Result;

	/**
	 * Visit a parse tree produced by `dnaorganismParser.attrPair`.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	visitAttrPair?: (ctx: AttrPairContext) => Result;
}

