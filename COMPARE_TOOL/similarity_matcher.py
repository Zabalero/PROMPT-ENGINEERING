"""
File Comparison Tool - Similarity Matching Algorithm

Implements text similarity comparison using difflib for line-by-line matching
with configurable similarity thresholds.
"""

import difflib
from typing import Dict, List, Tuple, Optional


class SimilarityMatcher:
    """Handles text similarity matching and comparison logic"""
    
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold
        self.left_lines = []
        self.right_lines = []
        self.matches = {}
        
    def set_threshold(self, threshold: float):
        """Update similarity threshold (0.0 to 1.0)"""
        self.threshold = max(0.0, min(1.0, threshold))
    
    def get_threshold(self) -> float:
        """Get current similarity threshold"""
        return self.threshold
    
    def compare_texts(self, left_text: str, right_text: str) -> Dict:
        """
        Compare two texts and return matching information
        
        Args:
            left_text: Content of left panel
            right_text: Content of right panel
            
        Returns:
            Dictionary mapping left line numbers to match info
        """
        if not left_text and not right_text:
            return {}
            
        # Split texts into lines
        self.left_lines = left_text.splitlines() if left_text else []
        self.right_lines = right_text.splitlines() if right_text else []
        
        # Find matches
        self.matches = self._find_best_matches()
        
        return self.matches
    
    def _find_best_matches(self) -> Dict:
        """
        Find optimal line matches using similarity threshold
        
        Returns:
            Dictionary with match information:
            {
                left_line_num: {
                    'right_line': right_line_num,
                    'similarity': similarity_score,
                    'match_type': 'exact'|'high'|'medium'|'low'
                }
            }
        """
        matches = {}
        used_right_lines = set()
        
        for left_idx, left_line in enumerate(self.left_lines):
            left_line_num = left_idx + 1  # 1-based line numbers
            best_match = None
            best_similarity = 0.0
            best_right_idx = -1
            
            # Find best matching right line
            for right_idx, right_line in enumerate(self.right_lines):
                if right_idx in used_right_lines:
                    continue
                
                similarity = self._calculate_line_similarity(left_line, right_line)
                
                if similarity >= self.threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = right_line
                    best_right_idx = right_idx
            
            # Store match if found
            if best_match is not None:
                matches[left_line_num] = {
                    'right_line': best_right_idx + 1,  # 1-based
                    'similarity': best_similarity,
                    'match_type': self._get_match_type(best_similarity),
                    'left_text': left_line,
                    'right_text': best_match
                }
                used_right_lines.add(best_right_idx)
        
        return matches
    
    def _calculate_line_similarity(self, line1: str, line2: str) -> float:
        """
        Calculate similarity ratio between two lines
        
        Args:
            line1: First line to compare
            line2: Second line to compare
            
        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        if not line1.strip() and not line2.strip():
            return 1.0  # Both empty lines are identical
        
        if not line1.strip() or not line2.strip():
            return 0.0  # One empty, one not
        
        # Use SequenceMatcher for similarity calculation
        matcher = difflib.SequenceMatcher(None, line1.strip(), line2.strip())
        return matcher.ratio()
    
    def _get_match_type(self, similarity: float) -> str:
        """
        Categorize match type based on similarity score
        
        Args:
            similarity: Similarity ratio (0.0 to 1.0)
            
        Returns:
            Match type: 'exact', 'high', 'medium', or 'low'
        """
        if similarity >= 0.99:
            return 'exact'
        elif similarity >= 0.9:
            return 'high'
        elif similarity >= 0.7:
            return 'medium'
        else:
            return 'low'
    
    def get_line_similarity(self, left_line_num: int, right_line_num: int) -> float:
        """
        Get similarity between specific line numbers
        
        Args:
            left_line_num: Line number in left panel (1-based)
            right_line_num: Line number in right panel (1-based)
            
        Returns:
            Similarity ratio (0.0 to 1.0)
        """
        if (left_line_num < 1 or left_line_num > len(self.left_lines) or
            right_line_num < 1 or right_line_num > len(self.right_lines)):
            return 0.0
        
        left_line = self.left_lines[left_line_num - 1]
        right_line = self.right_lines[right_line_num - 1]
        
        return self._calculate_line_similarity(left_line, right_line)
    
    def find_matching_line(self, left_line_num: int) -> Optional[int]:
        """
        Find matching line in right panel for given left line
        
        Args:
            left_line_num: Line number in left panel (1-based)
            
        Returns:
            Matching line number in right panel or None
        """
        if left_line_num in self.matches:
            return self.matches[left_line_num]['right_line']
        
        # Look for nearby matches if exact match not found
        return self._find_nearest_match(left_line_num)
    
    def _find_nearest_match(self, left_line_num: int, search_range: int = 5) -> Optional[int]:
        """
        Find nearest matching line within search range
        
        Args:
            left_line_num: Target left line number
            search_range: Number of lines to search before/after
            
        Returns:
            Nearest matching right line number or None
        """
        for offset in range(1, search_range + 1):
            # Check lines before
            if (left_line_num - offset) in self.matches:
                match_info = self.matches[left_line_num - offset]
                return match_info['right_line'] + offset
            
            # Check lines after
            if (left_line_num + offset) in self.matches:
                match_info = self.matches[left_line_num + offset]
                return match_info['right_line'] - offset
        
        return None
    
    def find_all_matches_for_line(self, left_line_content: str, right_lines: List[str]) -> List[Tuple[int, float]]:
        """
        Find all matches for a single line in a list of lines that meet the similarity threshold.

        Args:
            left_line_content: The content of the line to match.
            right_lines: A list of lines to search for a match.

        Returns:
            A list of tuples, where each tuple contains the line number (1-based) and similarity score
            of a match. The list is sorted by similarity score in descending order.
        """
        matches = []
        for i, right_line in enumerate(right_lines):
            similarity = self._calculate_line_similarity(left_line_content, right_line)
            if similarity >= self.threshold:
                matches.append((i + 1, similarity))

        # Sort matches by similarity score in descending order
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def get_match_statistics(self) -> Dict:
        """
        Get statistics about current matches
        
        Returns:
            Dictionary with match statistics
        """
        if not self.matches:
            return {
                'total_left_lines': len(self.left_lines),
                'total_right_lines': len(self.right_lines),
                'matched_lines': 0,
                'match_percentage': 0.0,
                'exact_matches': 0,
                'high_matches': 0,
                'medium_matches': 0,
                'low_matches': 0
            }
        
        # Count match types
        match_counts = {'exact': 0, 'high': 0, 'medium': 0, 'low': 0}
        for match_info in self.matches.values():
            match_type = match_info['match_type']
            match_counts[match_type] += 1
        
        total_matches = len(self.matches)
        match_percentage = (total_matches / len(self.left_lines) * 100) if self.left_lines else 0.0
        
        return {
            'total_left_lines': len(self.left_lines),
            'total_right_lines': len(self.right_lines),
            'matched_lines': total_matches,
            'match_percentage': match_percentage,
            'exact_matches': match_counts['exact'],
            'high_matches': match_counts['high'],
            'medium_matches': match_counts['medium'],
            'low_matches': match_counts['low']
        }
    
    def get_unmatched_left_lines(self) -> List[int]:
        """Get list of unmatched line numbers in left panel"""
        total_lines = len(self.left_lines)
        matched_lines = set(self.matches.keys())
        return [i for i in range(1, total_lines + 1) if i not in matched_lines]
    
    def get_unmatched_right_lines(self) -> List[int]:
        """Get list of unmatched line numbers in right panel"""
        total_lines = len(self.right_lines)
        matched_lines = {info['right_line'] for info in self.matches.values()}
        return [i for i in range(1, total_lines + 1) if i not in matched_lines]
    
    def update_line_content(self, panel: str, line_num: int, new_content: str):
        """
        Update line content and recalculate affected matches
        
        Args:
            panel: 'left' or 'right'
            line_num: Line number (1-based)
            new_content: New line content
        """
        if panel == 'left' and 1 <= line_num <= len(self.left_lines):
            self.left_lines[line_num - 1] = new_content
            # Recalculate matches for this line
            self._recalculate_line_matches(line_num, 'left')
        elif panel == 'right' and 1 <= line_num <= len(self.right_lines):
            self.right_lines[line_num - 1] = new_content
            # Recalculate matches for lines that reference this right line
            self._recalculate_right_line_matches(line_num)
    
    def _recalculate_line_matches(self, left_line_num: int, panel: str):
        """Recalculate matches for a specific line after content change"""
        if panel == 'left' and left_line_num in self.matches:
            # Remove old match
            old_right_line = self.matches[left_line_num]['right_line']
            del self.matches[left_line_num]
            
            # Find new best match
            left_line = self.left_lines[left_line_num - 1]
            best_match = None
            best_similarity = 0.0
            best_right_idx = -1
            
            # Get currently used right lines
            used_right_lines = {info['right_line'] - 1 for info in self.matches.values()}
            
            for right_idx, right_line in enumerate(self.right_lines):
                if right_idx in used_right_lines:
                    continue
                
                similarity = self._calculate_line_similarity(left_line, right_line)
                
                if similarity >= self.threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = right_line
                    best_right_idx = right_idx
            
            # Store new match if found
            if best_match is not None:
                self.matches[left_line_num] = {
                    'right_line': best_right_idx + 1,
                    'similarity': best_similarity,
                    'match_type': self._get_match_type(best_similarity),
                    'left_text': left_line,
                    'right_text': best_match
                }
    
    def _recalculate_right_line_matches(self, right_line_num: int):
        """Recalculate matches that reference a changed right line"""
        # Find left lines that match this right line
        affected_left_lines = []
        for left_line_num, match_info in self.matches.items():
            if match_info['right_line'] == right_line_num:
                affected_left_lines.append(left_line_num)
        
        # Recalculate matches for affected left lines
        for left_line_num in affected_left_lines:
            self._recalculate_line_matches(left_line_num, 'left')