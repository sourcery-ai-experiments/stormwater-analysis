from typing import Dict, List

import swmmio
from swmmio.utils.functions import trace_from_node

from stormwater_analysis.data.data import ConduitsData, NodesData, SubcatchmentsData
from stormwater_analysis.pipes.round import min_slope


class SwmmModel:
    """
    A class representing a Storm Water Management Model (SWMM) with processed data.

    Attributes:
        model (swmmio.Model): The original SWMM model.
        conduits_data (ConduitsData): The processed conduits data after feature engineering.
        nodes_data (NodesData): The processed nodes data after feature engineering.
        subcatchments_data (SubcatchmentsData): The processed subcatchments data after feature engineering.
    """

    def __init__(
        self,
        model: swmmio.Model,
        conduits_data: ConduitsData,
        nodes_data: NodesData,
        subcatchments_data: SubcatchmentsData,
    ) -> None:
        """
        Initializes a SwmmModel object with the given SWMM model and processed data.

        Args:
            model (swmmio.Model): The original SWMM model.
            conduits_data (ConduitsData): The processed conduits data after feature engineering.
            nodes_data (NodesData): The processed nodes data after feature engineering.
            subcatchments_data (SubcatchmentsData): The processed subcatchments data after feature engineering.
        """
        self.model = model
        self.conduits_data = conduits_data
        self.nodes_data = nodes_data
        self.subcatchments_data = subcatchments_data

    def find_all_traces(self) -> Dict[str, List[str]]:
        """
        Finds all traces in the SWMM model.

        A trace is a list of conduit IDs that connect a specific outfall to the rest of the network.

        Returns:
            Dict[str, List[str]]: A dictionary where the keys are outfall IDs and the values are lists
            of conduit IDs representing the traces connecting the outfalls to the rest of the network.
        """
        outfalls = self.model.inp.outfalls.index
        return {outfall: trace_from_node(self.conduits_data.conduits, outfall) for outfall in outfalls}

    def find_overflowing_pipes(self) -> Dict[str, List[str]]:
        """
        Finds all overflowing pipes in the SWMM model.
        
        1. Określić na których kanałach sieć jest przepełniona.
            * Zwróć liste kanałów, które są w koleumnie conduits['ValMaxFill'] == 0 
        2. Zwrócić lista kanałów, które są przepełnione.
            * zwrócić trasę kanałów, które są przepełnione na jednej sieci od ostatiego do pierwszego czyli odpłwy - dopływ
        """

    
    def place_pipes_to_apply_change(self) -> None:
        """
        Places pipes to apply a change in the SWMM model.

        1. Na podstawie listy przepełnionych kanałów określić
           gdzie należy zastosować rekomendowaną zmianę techniczną.
        2. Zwrócić liste kanałów lub studzienek na których zastosować zmianę. 
        """
    
    def generate_technical_recommendation(self) -> None:
        """
        Generates a technical recommendation in the SWMM model.
        
        1. Użyj wytrenowanego ANN do generowania rekomendacji technicznej.
        2. Przygotuj format danych w jakich bęziesz przechowywał rekomendację. 
        3. Zapisz dane do pliku.
        4. Zwrócić użytkownikowi rekomendację. 
        """

    def optimize_conduit_slope(self) -> None:
        # Currently, this function is not needed.
        # TODO: min_slope() returns a minimal slope as number/1000,  SlopeFtPerFt is a number.
        #       So we need to convert it to number/1000.
        #       SlopePerMile take number/1000, so there is no need to convert it to number/1000.
        self.conduits_data.conduits.SlopeFtPerFt = min_slope(
            filling=self.conduits_data.conduits.Filling,
            diameter=self.conduits_data.conduits.Geom1,
        )

    def optimize_conduit_depth(self):  # type: ignore
        # Currently, this function is not needed.
        pass

    def optimize_conduit_diameter(self):  # type: ignore
        # Currently, this function is not needed.
        pass

    def optimize(self):  # type: ignore
        # Currently, this function is not needed.
        pass
