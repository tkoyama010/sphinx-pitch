"""
sphinx-pitch: Minimal pitch directive for Reveal.js presentations
"""

import re
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class PitchNode(nodes.General, nodes.Element):
    pass


class PitchSlideNode(nodes.General, nodes.Element):
    pass


class PitchGridNode(nodes.General, nodes.Element):
    pass


# Regex to parse [drag=WIDTH HEIGHT, drop=POSITION, ...] syntax
DRAG_PATTERN = re.compile(
    r"\[drag=(\d+)\s+(\d+)(?:,\s*drop=(\w+))?(?:,\s*flow=(\w+))?(?:,\s*sync=(\w+))?\]"
)


class PitchDirective(SphinxDirective):
    has_content = True
    option_spec = {}

    def run(self):
        pitch_node = PitchNode()
        lines = list(self.content)

        # Split by ---
        slides = []
        current = []
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
            slide = PitchSlideNode()
            slide["slide_id"] = f"slide-{i + 1}"

            j = 0
            while j < len(slide_lines):
                line = slide_lines[j]
                stripped = line.strip()

                if not stripped:
                    j += 1
                    continue

                # Check for [drag=...] syntax
                drag_match = DRAG_PATTERN.match(stripped)
                if drag_match:
                    # Parse grid parameters
                    width = drag_match.group(1)
                    height = drag_match.group(2)
                    position = drag_match.group(3) or "left"
                    flow = drag_match.group(4) or ""
                    sync = drag_match.group(5) or ""

                    # Collect grid content until next drag directive or end of slide
                    grid_content = []
                    j += 1
                    while j < len(slide_lines):
                        next_line = slide_lines[j]
                        if DRAG_PATTERN.match(
                            next_line.strip()
                        ) or next_line.strip().startswith("# "):
                            break
                        if next_line.strip() == "---":
                            break
                        grid_content.append(next_line)
                        j += 1

                    # Create grid node
                    grid = PitchGridNode()
                    grid["width"] = width
                    grid["height"] = height
                    grid["position"] = position
                    grid["flow"] = flow
                    grid["sync"] = sync

                    # Process grid content
                    for content_line in grid_content:
                        content_stripped = content_line.strip()
                        if not content_stripped:
                            continue

                        if content_stripped.startswith("## "):
                            # Sub-heading
                            para = nodes.paragraph()
                            para["classes"] = ["pitch-subtitle"]
                            strong = nodes.strong()
                            strong += nodes.Text(content_stripped[3:])
                            para += strong
                            grid += para
                        elif content_stripped.startswith("- "):
                            # List item
                            para = nodes.paragraph()
                            para["classes"] = ["pitch-list-item"]
                            para += nodes.Text("• " + content_stripped[2:])
                            grid += para
                        else:
                            # Regular text
                            para = nodes.paragraph()
                            para += nodes.Text(content_stripped)
                            grid += para

                    slide += grid
                elif stripped.startswith("# "):
                    # Heading
                    para = nodes.paragraph()
                    para["classes"] = ["pitch-title"]
                    strong = nodes.strong()
                    strong += nodes.Text(stripped[2:])
                    para += strong
                    slide += para
                    j += 1
                else:
                    # Regular text
                    para = nodes.paragraph()
                    para += nodes.Text(stripped)
                    slide += para
                    j += 1

            pitch_node += slide

        return [pitch_node]


def visit_pitch_node(self, node):
    self.body.append('<div class="pitch-deck">')


def depart_pitch_node(self, node):
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


def visit_pitch_slide_node(self, node):
    self.body.append(f'<section class="pitch-slide" id="{node["slide_id"]}">')


def depart_pitch_slide_node(self, node):
    self.body.append("</section>")


def visit_pitch_grid_node(self, node):
    width = node.get("width", "50")
    height = node.get("height", "50")
    position = node.get("position", "left")
    flow = node.get("flow", "")
    sync = node.get("sync", "")

    # Calculate CSS properties based on position
    if position == "left":
        left = "0"
        right = "auto"
    elif position == "right":
        left = "auto"
        right = "0"
    elif position == "top":
        left = "0"
        right = "auto"
    elif position == "bottom":
        left = "0"
        right = "auto"
    else:
        left = "0"
        right = "auto"

    # Build style attribute
    styles = [
        f"width: {width}%",
        f"height: {height}%",
        f"position: absolute",
        f"left: {left}",
    ]

    if right != "auto":
        styles.append(f"right: {right}")

    if position in ["top", "bottom"]:
        styles.append(f"{position}: 0")

    if flow == "stack":
        styles.append("display: flex")
        styles.append("flex-direction: column")

    style_str = "; ".join(styles)
    self.body.append(f'<div class="pitch-grid" style="{style_str}">')


def depart_pitch_grid_node(self, node):
    self.body.append("</div>")


def setup(app: Sphinx):
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
