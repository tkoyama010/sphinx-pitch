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
# Supports: drag=100px 200px or drag=50% 80% (default: %)
# Supports: drop=left/right/top/bottom/center or drop=100px 200px
DRAG_PATTERN = re.compile(
    r"\[drag=(\d+)(px|%)?\s+(\d+)(px|%)?(?:,\s*drop=(?:(left|right|top|bottom|center)|(\d+)(px|%)?\s+(\d+)(px|%)?))?(?:,\s*flow=(\w+))?(?:,\s*sync=(\w+))?(?:,\s*bg=([#\w]+))?\]"
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

        # Get grid size from config (conf.py)
        config = self.env.config
        grid_size = getattr(config, "pitch_grid_size", "")

        # Store grid_size in pitch_node for use in visit_pitch_node
        pitch_node["grid"] = grid_size

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
                    width_val = drag_match.group(1)
                    width_unit = drag_match.group(2) or "%"
                    height_val = drag_match.group(3)
                    height_unit = drag_match.group(4) or "%"

                    # Build width/height with units
                    width = f"{width_val}{width_unit}"
                    height = f"{height_val}{height_unit}"

                    # Parse drop - either keyword or coordinates
                    drop_keyword = drag_match.group(5)
                    drop_x_val = drag_match.group(6)
                    drop_x_unit = drag_match.group(7) or "px"
                    drop_y_val = drag_match.group(8)
                    drop_y_unit = drag_match.group(9) or "px"

                    if drop_keyword:
                        # Using keyword position
                        position = drop_keyword
                        drop_x = None
                        drop_y = None
                    elif drop_x_val and drop_y_val:
                        # Using pixel/percentage coordinates
                        position = "coords"
                        drop_x = f"{drop_x_val}{drop_x_unit}"
                        drop_y = f"{drop_y_val}{drop_y_unit}"
                    else:
                        position = "left"
                        drop_x = None
                        drop_y = None

                    flow = drag_match.group(10) or ""
                    sync = drag_match.group(11) or ""
                    bg = drag_match.group(12) or ""

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
                    grid["drop_x"] = drop_x or ""
                    grid["drop_y"] = drop_y or ""
                    grid["flow"] = flow
                    grid["sync"] = sync
                    grid["bg"] = bg

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
    grid_size = node.get("grid", "")
    grid_html = ""
    if grid_size:
        # Add simple container for grid (JavaScript will populate it)
        grid_html = '<div class="pitch-grid-overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;"></div>'
    self.body.append(f'<div class="pitch-deck">{grid_html}')


def depart_pitch_node(self, node):
    grid_size = node.get("grid", "")
    grid_script = ""
    if grid_size:
        # Add JavaScript to dynamically generate grid with numbers
        grid_script = f"""
<script>
(function(){{
var deck=document.currentScript.closest('.pitch-deck');
var gridOverlay=deck.querySelector('.pitch-grid-overlay');
if(gridOverlay){{
var gridSize={grid_size};
var width=deck.offsetWidth;
var height=deck.offsetHeight;
var svgNS="http://www.w3.org/2000/svg";
var svg=document.createElementNS(svgNS,"svg");
svg.setAttribute("width",width);
svg.setAttribute("height",height);
svg.style.position="absolute";
svg.style.top="0";
svg.style.left="0";
svg.style.pointerEvents="none";
// Grid lines
for(var x=0;x<=width;x+=gridSize){{
var line=document.createElementNS(svgNS,"line");
line.setAttribute("x1",x);
line.setAttribute("y1",0);
line.setAttribute("x2",x);
line.setAttribute("y2",height);
line.setAttribute("stroke","rgba(255,255,255,0.3)");
line.setAttribute("stroke-width","1");
svg.appendChild(line);
// X-axis numbers
if(x>0){{
var text=document.createElementNS(svgNS,"text");
text.setAttribute("x",x);
text.setAttribute("y",15);
text.setAttribute("text-anchor","middle");
text.setAttribute("fill","white");
text.setAttribute("font-size","10");
text.textContent=x;
svg.appendChild(text);
}}
}}
for(var y=0;y<=height;y+=gridSize){{
var line=document.createElementNS(svgNS,"line");
line.setAttribute("x1",0);
line.setAttribute("y1",y);
line.setAttribute("x2",width);
line.setAttribute("y2",y);
line.setAttribute("stroke","rgba(255,255,255,0.3)");
line.setAttribute("stroke-width","1");
svg.appendChild(line);
// Y-axis numbers
if(y>0){{
var text=document.createElementNS(svgNS,"text");
text.setAttribute("x",25);
text.setAttribute("y",y+3);
text.setAttribute("text-anchor","middle");
text.setAttribute("fill","white");
text.setAttribute("font-size","10");
text.textContent=y;
svg.appendChild(text);
}}
}}
// Background for rulers
var rulerBg=document.createElementNS(svgNS,"rect");
rulerBg.setAttribute("x",0);
rulerBg.setAttribute("y",0);
rulerBg.setAttribute("width",width);
rulerBg.setAttribute("height",20);
rulerBg.setAttribute("fill","rgba(0,0,0,0.7)");
svg.appendChild(rulerBg);
var rulerBg2=document.createElementNS(svgNS,"rect");
rulerBg2.setAttribute("x",0);
rulerBg2.setAttribute("y",0);
rulerBg2.setAttribute("width",50);
rulerBg2.setAttribute("height",height);
rulerBg2.setAttribute("fill","rgba(0,0,0,0.7)");
svg.appendChild(rulerBg2);
gridOverlay.appendChild(svg);
}}
}})();
</script>"""
    self.body.append(f"""
<script>
(function(){{
var deck=document.currentScript.closest('.pitch-deck');
var slides=deck.querySelectorAll('.pitch-slide');
var current=0;
function show(){{slides.forEach((s,i)=>s.style.display=i===current?'block':'none');}}
function next(){{if(current<slides.length-1){{current++;show();}}}}
function prev(){{if(current>0){{current--;show();}}}}
document.addEventListener('keydown',function(e){{
if(e.key==='ArrowRight'||e.key===' ')next();
if(e.key==='ArrowLeft')prev();
}});
show();
}})();
</script>{grid_script}
</div>""")


def visit_pitch_slide_node(self, node):
    self.body.append(f'<section class="pitch-slide" id="{node["slide_id"]}">')


def depart_pitch_slide_node(self, node):
    self.body.append("</section>")


def visit_pitch_grid_node(self, node):
    width = node.get("width", "50%")
    height = node.get("height", "50%")
    position = node.get("position", "left")
    drop_x = node.get("drop_x", "")
    drop_y = node.get("drop_y", "")
    flow = node.get("flow", "")
    sync = node.get("sync", "")
    bg = node.get("bg", "")

    # Build style attribute
    styles = [
        f"width: {width}",
        f"height: {height}",
        f"position: absolute",
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
    # Add config value for grid size (can be set in conf.py)
    app.add_config_value("pitch_grid_size", "", "env")
    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
