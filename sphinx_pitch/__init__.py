"""sphinx-pitch: Minimal pitch directive for Reveal.js presentations."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar

from docutils import nodes
from sphinx.util.docutils import SphinxDirective

if TYPE_CHECKING:
    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.writers.html import HTMLTranslator


class PitchNode(nodes.General, nodes.Element):
    """Root node for pitch presentation deck."""


class PitchSlideNode(nodes.General, nodes.Element):
    """Node representing a single pitch slide."""


class PitchGridNode(nodes.General, nodes.Element):
    """Node representing a grid element within a slide."""


# Regex to parse [drag=WIDTH HEIGHT, drop=POSITION, ...] syntax
# Supports: drag=100px 200px or drag=50% 80% (default: %)
# Supports: drop=left/right/top/bottom/center or drop=100px 200px
DRAG_PATTERN = re.compile(
    r"\[drag=(\d+)(px|%)?\s+(\d+)(px|%)?(?:,\s*drop=(?:(left|right|top|bottom|center)|(\d+)(px|%)?\s+(\d+)(px|%)?))?(?:,\s*flow=(\w+))?(?:,\s*sync=(\w+))?(?:,\s*bg=([#\w]+))?\]"
)


class PitchDirective(SphinxDirective):
    """Directive for creating pitch presentations."""

    has_content = True
    option_spec: ClassVar[dict[str, type]] = {}

    def run(self) -> list[Node]:
        """Process the pitch directive content and return nodes."""
        return self._process_pitch()

    def _process_pitch(self) -> list[Node]:
        """Parse pitch content and build node tree."""
        pitch_node = PitchNode()
        lines = list(self.content)

        # Split by ---
        slides: list[list[str]] = []
        current: list[str] = []
        for line in lines:
            if line.strip() == "---":
                if current:
                    slides.append(current)
                    current = []
            else:
                current.append(line)
        if current:
            slides.append(current)

        for i, slide_lines in enumerate(slides):
            slide = self._create_slide(i, slide_lines)
            pitch_node += slide

        return [pitch_node]

    def _create_slide(self, slide_idx: int, slide_lines: list[str]) -> PitchSlideNode:
        """Create a single slide from parsed lines."""
        slide = PitchSlideNode()
        slide["slide_id"] = f"slide-{slide_idx + 1}"

        j = 0
        while j < len(slide_lines):
            line = slide_lines[j]
            stripped = line.strip()

            if not stripped:
                j += 1
                continue

            j = self._process_slide_line(slide, slide_lines, j, stripped)

        return slide

    def _process_slide_line(
        self,
        slide: PitchSlideNode,
        slide_lines: list[str],
        idx: int,
        stripped: str,
    ) -> int:
        """Process a single line within a slide."""
        # Check for [drag=...] syntax
        drag_match = DRAG_PATTERN.match(stripped)
        if drag_match:
            return self._process_drag_directive(slide, slide_lines, idx, drag_match)

        if stripped.startswith("# "):
            # Heading
            para = nodes.paragraph()
            para["classes"] = ["pitch-title"]
            strong = nodes.strong()
            strong += nodes.Text(stripped[2:])
            para += strong
            slide += para
            return idx + 1

        # Regular text
        para = nodes.paragraph()
        para += nodes.Text(stripped)
        slide += para
        return idx + 1

    def _process_drag_directive(
        self,
        slide: PitchSlideNode,
        slide_lines: list[str],
        idx: int,
        drag_match: re.Match[str],
    ) -> int:
        """Process a drag directive and create grid node."""
        grid = self._create_grid_node(drag_match)
        j = self._collect_grid_content(slide_lines, idx, grid)
        self._process_grid_content(grid)
        slide += grid
        return j

    def _create_grid_node(self, drag_match: re.Match[str]) -> PitchGridNode:
        """Create grid node from drag directive match."""
        width_val = drag_match.group(1)
        width_unit = drag_match.group(2) or "%"
        height_val = drag_match.group(3)
        height_unit = drag_match.group(4) or "%"

        width = f"{width_val}{width_unit}"
        height = f"{height_val}{height_unit}"

        drop_keyword = drag_match.group(5)
        drop_x_val = drag_match.group(6)
        drop_x_unit = drag_match.group(7) or "px"
        drop_y_val = drag_match.group(8)
        drop_y_unit = drag_match.group(9) or "px"

        if drop_keyword:
            position = drop_keyword
            drop_x = None
            drop_y = None
        elif drop_x_val and drop_y_val:
            position = "coords"
            drop_x = f"{drop_x_val}{drop_x_unit}"
            drop_y = f"{drop_y_val}{drop_y_unit}"
        else:
            position = "left"
            drop_x = None
            drop_y = None

        grid = PitchGridNode()
        grid["width"] = width
        grid["height"] = height
        grid["position"] = position
        grid["drop_x"] = drop_x or ""
        grid["drop_y"] = drop_y or ""
        grid["flow"] = drag_match.group(10) or ""
        grid["sync"] = drag_match.group(11) or ""
        grid["bg"] = drag_match.group(12) or ""

        return grid

    def _collect_grid_content(
        self,
        slide_lines: list[str],
        idx: int,
        grid: PitchGridNode,
    ) -> int:
        """Collect content lines for grid node."""
        grid_content = []
        j = idx + 1
        while j < len(slide_lines):
            next_line = slide_lines[j]
            if DRAG_PATTERN.match(next_line.strip()) or next_line.strip().startswith(
                "# "
            ):
                break
            if next_line.strip() == "---":
                break
            grid_content.append(next_line)
            j += 1

        grid["content"] = grid_content
        return j

    def _process_grid_content(self, grid: PitchGridNode) -> None:
        """Process collected grid content and add to node."""
        content: list[str] = grid.get("content", [])
        for content_line in content:
            content_stripped: str = content_line.strip()
            if not content_stripped:
                continue

            if content_stripped.startswith("## "):
                self._add_subheading(grid, content_stripped[3:])
            elif content_stripped.startswith("- "):
                self._add_list_item(grid, content_stripped[2:])
            else:
                self._add_text(grid, content_stripped)

    def _add_subheading(self, grid: PitchGridNode, text: str) -> None:
        """Add subheading paragraph to grid."""
        para = nodes.paragraph()
        para["classes"] = ["pitch-subtitle"]
        strong = nodes.strong()
        strong += nodes.Text(text)
        para += strong
        grid += para

    def _add_list_item(self, grid: PitchGridNode, text: str) -> None:
        """Add list item paragraph to grid."""
        para = nodes.paragraph()
        para["classes"] = ["pitch-list-item"]
        para += nodes.Text("• " + text)
        grid += para

    def _add_text(self, grid: PitchGridNode, text: str) -> None:
        """Add text paragraph to grid."""
        para = nodes.paragraph()
        para += nodes.Text(text)
        grid += para


def visit_pitch_node(self: HTMLTranslator, _node: Node) -> None:
    """Visit pitch node and start HTML container."""
    self.body.append('<div class="pitch-deck">')


def depart_pitch_node(self: HTMLTranslator, _node: Node) -> None:
    """Depart pitch node and add navigation script."""
    self.body.append(
        """
<script>
(function(){
var deck=document.currentScript.closest('.pitch-deck');
var slides=deck.querySelectorAll('.pitch-slide');
var current=0;
function show(){slides.forEach((s,i)=>s.style.display=i===current?'block':'none');}
function next(){if(current<slides.length-1){current++;show();}}
function prev(){if(current>0){current--;show();}}
document.addEventListener('keydown',function(e){
if(e.key==='ArrowRight'||e.key===' ')next();
if(e.key==='ArrowLeft')prev();
});
show();
})();
</script>
</div>"""
    )


def visit_pitch_slide_node(self: HTMLTranslator, node: PitchSlideNode) -> None:
    """Visit pitch slide node and start section."""
    self.body.append(f'<section class="pitch-slide" id="{node["slide_id"]}">')


def depart_pitch_slide_node(self: HTMLTranslator, _node: Node) -> None:
    """Depart pitch slide node and close section."""
    self.body.append("</section>")


def visit_pitch_grid_node(self: HTMLTranslator, node: PitchGridNode) -> None:
    """Visit pitch grid node and create positioned div."""
    width = node.get("width", "50%")
    height = node.get("height", "50%")
    position = node.get("position", "left")
    drop_x = node.get("drop_x", "")
    drop_y = node.get("drop_y", "")
    flow = node.get("flow", "")
    bg = node.get("bg", "")

    # Build style attribute
    styles = [
        f"width: {width}",
        f"height: {height}",
        "position: absolute",
    ]

    # Calculate position
    if position == "coords" and drop_x and drop_y:
        # Pixel/percentage coordinates
        styles.append(f"left: {drop_x}")
        styles.append(f"top: {drop_y}")
    elif position == "left":
        styles.append("left: 0")
        styles.append("top: 0")
    elif position == "right":
        styles.append("right: 0")
        styles.append("top: 0")
    elif position == "top":
        styles.append("left: 0")
        styles.append("top: 0")
    elif position == "bottom":
        styles.append("left: 0")
        styles.append("bottom: 0")
    elif position == "center":
        styles.append("left: 50%")
        styles.append("top: 50%")
        styles.append("transform: translate(-50%, -50%)")
    else:
        styles.append("left: 0")
        styles.append("top: 0")

    if flow == "stack":
        styles.append("display: flex")
        styles.append("flex-direction: column")

    if bg:
        styles.append(f"background-color: {bg}")

    style_str = "; ".join(styles)
    self.body.append(f'<div class="pitch-grid" style="{style_str}">')


def depart_pitch_grid_node(self: HTMLTranslator, _node: Node) -> None:
    """Depart pitch grid node and close div."""
    self.body.append("</div>")


def setup(app: Sphinx) -> dict[str, str | bool]:
    """Set up the sphinx-pitch extension."""
    app.add_directive("pitch", PitchDirective)
    app.add_node(
        PitchNode,
        html=(visit_pitch_node, depart_pitch_node),
    )
    app.add_node(
        PitchSlideNode,
        html=(visit_pitch_slide_node, depart_pitch_slide_node),
    )
    app.add_node(
        PitchGridNode,
        html=(visit_pitch_grid_node, depart_pitch_grid_node),
    )
    app.add_css_file("pitch.css")
    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
