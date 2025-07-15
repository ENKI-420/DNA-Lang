// Generated from grammar/dnaorganism.g4 by ANTLR 4.9.0-SNAPSHOT


import { ParseTreeListener } from "antlr4ts/tree/ParseTreeListener";

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
 * This interface defines a complete listener for a parse tree produced by
 * `dnaorganismParser`.
 */
export interface dnaorganismListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by `dnaorganismParser.program`.
	 * @param ctx the parse tree
	 */
	enterProgram?: (ctx: ProgramContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.program`.
	 * @param ctx the parse tree
	 */
	exitProgram?: (ctx: ProgramContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.organismDef`.
	 * @param ctx the parse tree
	 */
	enterOrganismDef?: (ctx: OrganismDefContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.organismDef`.
	 * @param ctx the parse tree
	 */
	exitOrganismDef?: (ctx: OrganismDefContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.dnaBlock`.
	 * @param ctx the parse tree
	 */
	enterDnaBlock?: (ctx: DnaBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.dnaBlock`.
	 * @param ctx the parse tree
	 */
	exitDnaBlock?: (ctx: DnaBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.genomeBlock`.
	 * @param ctx the parse tree
	 */
	enterGenomeBlock?: (ctx: GenomeBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.genomeBlock`.
	 * @param ctx the parse tree
	 */
	exitGenomeBlock?: (ctx: GenomeBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.geneDef`.
	 * @param ctx the parse tree
	 */
	enterGeneDef?: (ctx: GeneDefContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.geneDef`.
	 * @param ctx the parse tree
	 */
	exitGeneDef?: (ctx: GeneDefContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.geneBody`.
	 * @param ctx the parse tree
	 */
	enterGeneBody?: (ctx: GeneBodyContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.geneBody`.
	 * @param ctx the parse tree
	 */
	exitGeneBody?: (ctx: GeneBodyContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.mutationsBlock`.
	 * @param ctx the parse tree
	 */
	enterMutationsBlock?: (ctx: MutationsBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.mutationsBlock`.
	 * @param ctx the parse tree
	 */
	exitMutationsBlock?: (ctx: MutationsBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.mutationDef`.
	 * @param ctx the parse tree
	 */
	enterMutationDef?: (ctx: MutationDefContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.mutationDef`.
	 * @param ctx the parse tree
	 */
	exitMutationDef?: (ctx: MutationDefContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.immuneBlock`.
	 * @param ctx the parse tree
	 */
	enterImmuneBlock?: (ctx: ImmuneBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.immuneBlock`.
	 * @param ctx the parse tree
	 */
	exitImmuneBlock?: (ctx: ImmuneBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.adaptiveBlock`.
	 * @param ctx the parse tree
	 */
	enterAdaptiveBlock?: (ctx: AdaptiveBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.adaptiveBlock`.
	 * @param ctx the parse tree
	 */
	exitAdaptiveBlock?: (ctx: AdaptiveBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.agentsBlock`.
	 * @param ctx the parse tree
	 */
	enterAgentsBlock?: (ctx: AgentsBlockContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.agentsBlock`.
	 * @param ctx the parse tree
	 */
	exitAgentsBlock?: (ctx: AgentsBlockContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.agentAssign`.
	 * @param ctx the parse tree
	 */
	enterAgentAssign?: (ctx: AgentAssignContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.agentAssign`.
	 * @param ctx the parse tree
	 */
	exitAgentAssign?: (ctx: AgentAssignContext) => void;

	/**
	 * Enter a parse tree produced by `dnaorganismParser.attrPair`.
	 * @param ctx the parse tree
	 */
	enterAttrPair?: (ctx: AttrPairContext) => void;
	/**
	 * Exit a parse tree produced by `dnaorganismParser.attrPair`.
	 * @param ctx the parse tree
	 */
	exitAttrPair?: (ctx: AttrPairContext) => void;
}

