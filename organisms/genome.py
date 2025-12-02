"""
Genome: DNA Sequence Encoding

Represents the genetic code of software organisms,
including genes that define behavior and mutations.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
import hashlib
import json


@dataclass
class Gene:
    """
    A single gene in the genome.
    
    Attributes:
        name: Gene identifier
        sequence: Encoded behavior (code/configuration)
        expression_level: How strongly gene is expressed (0-1)
        mutations: Accumulated mutations
        dominant: Whether gene is dominant
    """
    name: str
    sequence: str
    expression_level: float = 1.0
    mutations: List[str] = field(default_factory=list)
    dominant: bool = True
    
    def mutate(self, mutation: str) -> None:
        """Apply a mutation to this gene."""
        self.mutations.append(mutation)
        self.sequence = f"{self.sequence}|{mutation}"
    
    def get_hash(self) -> str:
        """Get hash of gene sequence."""
        return hashlib.md5(self.sequence.encode()).hexdigest()[:8]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "sequence": self.sequence,
            "expression_level": self.expression_level,
            "mutations": self.mutations,
            "dominant": self.dominant,
        }


@dataclass
class Genome:
    """
    Complete genome of an organism.
    
    Represents the full genetic code including:
    - Core genes (essential for survival)
    - Feature genes (optional capabilities)
    - Mutation history
    """
    
    organism_type: str
    genes: Dict[str, Gene] = field(default_factory=dict)
    generation: int = 0
    parent_genome_hash: Optional[str] = None
    
    def add_gene(self, gene: Gene) -> None:
        """Add a gene to the genome."""
        self.genes[gene.name] = gene
    
    def get_gene(self, name: str) -> Optional[Gene]:
        """Get gene by name."""
        return self.genes.get(name)
    
    def remove_gene(self, name: str) -> bool:
        """Remove gene from genome."""
        if name in self.genes:
            del self.genes[name]
            return True
        return False
    
    def mutate_gene(self, name: str, mutation: str) -> bool:
        """Apply mutation to specific gene."""
        gene = self.genes.get(name)
        if gene:
            gene.mutate(mutation)
            return True
        return False
    
    def express(self) -> Dict[str, float]:
        """
        Get expression levels of all genes.
        
        Returns:
            Dict mapping gene name to expression level
        """
        return {
            name: gene.expression_level
            for name, gene in self.genes.items()
        }
    
    def get_hash(self) -> str:
        """Get hash of entire genome."""
        gene_hashes = sorted(g.get_hash() for g in self.genes.values())
        combined = "|".join(gene_hashes)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def clone(self) -> "Genome":
        """Create a clone of this genome."""
        new_genome = Genome(
            organism_type=self.organism_type,
            generation=self.generation + 1,
            parent_genome_hash=self.get_hash(),
        )
        
        for name, gene in self.genes.items():
            new_gene = Gene(
                name=gene.name,
                sequence=gene.sequence,
                expression_level=gene.expression_level,
                mutations=gene.mutations.copy(),
                dominant=gene.dominant,
            )
            new_genome.add_gene(new_gene)
        
        return new_genome
    
    def crossover(self, other: "Genome") -> "Genome":
        """
        Create offspring genome through crossover.
        
        Args:
            other: Other parent genome
            
        Returns:
            New genome combining genes from both parents
        """
        offspring = Genome(
            organism_type=self.organism_type,
            generation=max(self.generation, other.generation) + 1,
        )
        
        # Take dominant genes from each parent
        all_genes = set(self.genes.keys()) | set(other.genes.keys())
        
        for name in all_genes:
            gene1 = self.genes.get(name)
            gene2 = other.genes.get(name)
            
            if gene1 and gene2:
                # Both have gene: take dominant or average
                if gene1.dominant and not gene2.dominant:
                    offspring.add_gene(Gene(
                        name=name,
                        sequence=gene1.sequence,
                        expression_level=gene1.expression_level,
                        dominant=True,
                    ))
                elif gene2.dominant and not gene1.dominant:
                    offspring.add_gene(Gene(
                        name=name,
                        sequence=gene2.sequence,
                        expression_level=gene2.expression_level,
                        dominant=True,
                    ))
                else:
                    # Mix
                    offspring.add_gene(Gene(
                        name=name,
                        sequence=f"{gene1.sequence[:len(gene1.sequence)//2]}{gene2.sequence[len(gene2.sequence)//2:]}",
                        expression_level=(gene1.expression_level + gene2.expression_level) / 2,
                        dominant=gene1.dominant or gene2.dominant,
                    ))
            elif gene1:
                offspring.add_gene(Gene(
                    name=name,
                    sequence=gene1.sequence,
                    expression_level=gene1.expression_level,
                    dominant=gene1.dominant,
                ))
            elif gene2:
                offspring.add_gene(Gene(
                    name=name,
                    sequence=gene2.sequence,
                    expression_level=gene2.expression_level,
                    dominant=gene2.dominant,
                ))
        
        return offspring
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "organism_type": self.organism_type,
            "genes": {name: gene.to_dict() for name, gene in self.genes.items()},
            "generation": self.generation,
            "parent_genome_hash": self.parent_genome_hash,
            "hash": self.get_hash(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Genome":
        """Deserialize from dictionary."""
        genome = cls(
            organism_type=data["organism_type"],
            generation=data.get("generation", 0),
            parent_genome_hash=data.get("parent_genome_hash"),
        )
        
        for name, gene_data in data.get("genes", {}).items():
            genome.add_gene(Gene(
                name=name,
                sequence=gene_data["sequence"],
                expression_level=gene_data.get("expression_level", 1.0),
                mutations=gene_data.get("mutations", []),
                dominant=gene_data.get("dominant", True),
            ))
        
        return genome
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Genome":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))
