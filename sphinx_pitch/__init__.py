"""
sphinx-pitch: Minimal pitch directive for Reveal.js presentations
"""

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class PitchNode(nodes.General, nodes.Element):
    pass


class PitchSlideNode(nodes.General, nodes.Element):
    pass


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

            # Add content as paragraphs
            for line in slide_lines:
                stripped = line.strip()
                if not stripped:
                    continue

                if stripped.startswith("# "):
                    # Heading
                    para = nodes.paragraph()
                    para["classes"] = ["pitch-title"]
                    strong = nodes.strong()
                    strong += nodes.Text(stripped[2:])
                    para += strong
                    slide += para
                else:
                    # Regular text
                    para = nodes.paragraph()
                    para += nodes.Text(stripped)
                    slide += para

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
    app.add_css_file("pitch.css")
    return {"version": "0.1.0", "parallel_read_safe": True, "parallel_write_safe": True}
