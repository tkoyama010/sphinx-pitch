"""
sphinx-pitch: A Sphinx extension for creating presentations like GitPitch.
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


class PitchFloatNode(nodes.General, nodes.Element):
    pass


class PitchCodeNode(nodes.General, nodes.Element):
    pass


class PitchListNode(nodes.General, nodes.Element):
    pass


class PitchNoteNode(nodes.General, nodes.Element):
    pass


def visit_pitch_node(self, node):
    self.body.append('<div class="pitch-presentation">')
    self.body.append('<div class="pitch-slides">')


def depart_pitch_node(self, node):
    self.body.append("</div>")  # Close pitch-slides

    # Add controls and JavaScript
    self.body.append("""
<div class="pitch-controls">
    <button class="pitch-prev" onclick="pitchPrev(this)">← Previous</button>
    <span class="pitch-slide-number">1 / 1</span>
    <button class="pitch-next" onclick="pitchNext(this)">Next →</button>
</div>
<script>
(function(){
function init(){
    var p=document.currentScript.closest('.pitch-presentation');
    var s=p.querySelectorAll('.pitch-slide');
    var n=p.querySelector('.pitch-slide-number');
    var b=p.querySelector('.pitch-prev');
    var f=p.querySelector('.pitch-next');
    var c=0,t=s.length;
    function u(){
        s.forEach(function(e,i){e.classList.toggle('active',i===c);});
        if(n)n.textContent=(c+1)+' / '+t;
        if(b)b.disabled=c===0;
        if(f)f.disabled=c===t-1;
    }
    window.pitchPrev=function(){if(c>0){c--;u();}};
    window.pitchNext=function(){if(c<t-1){c++;u();}};
    document.addEventListener('keydown',function(e){
        if(e.key==='ArrowLeft')pitchPrev();
        else if(e.key==='ArrowRight'||e.key===' ')pitchNext();
    });
    u();
}
init();
})();
</script>
</div>""")


def visit_pitch_slide_node(self, node):
    slide_id = node.get("slide_id", "")
    self.body.append(f'<section class="pitch-slide" id="{slide_id}">')


def depart_pitch_slide_node(self, node):
    self.body.append("</section>")


def visit_pitch_float_node(self, node):
    attrs = node.get("attrs", {})
    styles = ["position:absolute;"]
    classes = ["pitch-grid-block"]

    drag = attrs.get("drag", "")
    if drag:
        parts = drag.split()
        if len(parts) >= 1:
            w = parts[0]
            styles.append(f"width:{w}{'%' if w.isdigit() else ''};")
        if len(parts) >= 2:
            h = parts[1]
            styles.append(f"height:{h}{'%' if h.isdigit() else ''};")

    drop = attrs.get("drop", "")
    if drop in [
        "center",
        "left",
        "right",
        "top",
        "bottom",
        "topleft",
        "topright",
        "bottomleft",
        "bottomright",
    ]:
        classes.append(f"drop-{drop}")
    elif drop:
        parts = drop.split()
        if len(parts) >= 1:
            x = parts[0]
            styles.append(f"left:{x}{'%' if x.isdigit() else ''};")
        if len(parts) >= 2:
            y = parts[1]
            styles.append(f"top:{y}{'%' if y.isdigit() else ''};")

    if attrs.get("fit"):
        styles.append(f"--pitch-fit:{attrs['fit']};")
    if attrs.get("bg"):
        styles.append(f"background-color:{attrs['bg']};")
    if attrs.get("flow"):
        classes.append(f"flow-{attrs['flow']}")

    style_attr = " ".join(styles)
    class_attr = " ".join(classes)
    self.body.append(f'<div class="{class_attr}" style="{style_attr}">')


def depart_pitch_float_node(self, node):
    self.body.append("</div>")


def visit_pitch_code_node(self, node):
    import html as html_module

    attrs = node.get("attrs", {})
    lang = attrs.get("language", "text")
    content = node.get("content", "")
    escaped = html_module.escape(content)
    self.body.append(
        f'<div class="pitch-code-widget"><pre><code class="language-{lang}">{escaped}</code></pre></div>'
    )


def depart_pitch_code_node(self, node):
    pass


def visit_pitch_list_node(self, node):
    list_type = node.get("list_type", "ul")
    classes = node.get("classes", [])
    class_attr = " ".join(classes + ["pitch-list-widget"])

    if list_type == "ol":
        self.body.append(f'<ol class="{class_attr}">')
    else:
        self.body.append(f'<ul class="{class_attr}">')

    for item in node.get("items", []):
        self.body.append(f"<li>{item}</li>")


def depart_pitch_list_node(self, node):
    list_type = node.get("list_type", "ul")
    self.body.append("</ol>" if list_type == "ol" else "</ul>")


def visit_pitch_note_node(self, node):
    self.body.append('<aside class="pitch-notes" style="display:none;">')
    content = node.get("content", "")
    if content:
        self.body.append(content)


def depart_pitch_note_node(self, node):
    self.body.append("</aside>")


class PitchDirective(SphinxDirective):
    has_content = True
    option_spec = {
        "theme": directives.unchanged,
        "transition": directives.unchanged,
    }

    def run(self):
        pitch_node = PitchNode()
        pitch_node["options"] = self.options

        # Get all content lines
        lines = list(self.content)

        # Split into slides by ---
        slides_content = []
        current_slide = []

        for line in lines:
            if line.strip() == "---":
                if current_slide:
                    slides_content.append(current_slide)
                    current_slide = []
            else:
                current_slide.append(line)

        # Add last slide
        if current_slide:
            slides_content.append(current_slide)

        # Parse each slide
        for i, slide_lines in enumerate(slides_content):
            slide_node = PitchSlideNode()
            slide_node["slide_id"] = f"slide-{i + 1}"
            self._parse_slide(slide_node, slide_lines)
            pitch_node += slide_node

        return [pitch_node]

    def _parse_slide(self, slide_node, lines):
        """Parse slide content line by line."""
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                continue

            # Check for widgets first
            if stripped.startswith("@code["):
                i = self._parse_code_widget(slide_node, lines, i)
            elif stripped.startswith("@ul") or stripped.startswith("@ol"):
                i = self._parse_list_widget(slide_node, lines, i)
            elif stripped.startswith("@math"):
                i = self._parse_math_widget(slide_node, lines, i)
            elif stripped.startswith("Note:"):
                i = self._parse_note(slide_node, lines, i)
            elif stripped.startswith("[") and "drag=" in stripped:
                i = self._parse_float_block(slide_node, lines, i)
            else:
                # Regular content
                self._add_content(slide_node, stripped)
                i += 1

    def _parse_code_widget(self, parent, lines, start_idx):
        """Parse @code widget."""
        header = lines[start_idx].strip()
        match = re.match(r"@code\[([^\]]*)\]", header)
        attrs = {}

        if match:
            attr_str = match.group(1)
            parts = [p.strip() for p in attr_str.split(",")]
            # First part without = is language
            for p in parts:
                if "=" in p:
                    k, v = p.split("=", 1)
                    attrs[k.strip()] = v.strip()
                elif p and "language" not in attrs:
                    attrs["language"] = p

        # Collect code content until next widget or empty line or end
        code_lines = []
        i = start_idx + 1
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            # Stop at next widget, slide delimiter, or empty line after content
            if (
                stripped.startswith("@")
                or stripped.startswith("[")
                or stripped == "---"
            ):
                break
            if not stripped and code_lines:
                i += 1
                break
            if stripped.startswith("Note:"):
                break
            code_lines.append(line)
            i += 1

        node = PitchCodeNode()
        node["attrs"] = attrs
        node["content"] = "\n".join(code_lines)
        parent += node

        return i

    def _parse_list_widget(self, parent, lines, start_idx):
        """Parse @ul or @ol widget."""
        header = lines[start_idx].strip()
        list_type = "ol" if header.startswith("@ol") else "ul"

        # Parse classes
        match = re.match(r"@(?:ul|ol)\[([^\]]*)\]", header)
        classes = []
        if match:
            for part in match.group(1).split(","):
                part = part.strip()
                if part and "=" not in part:
                    classes.append(part)

        # Collect list items
        items = []
        i = start_idx + 1
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Stop at closing tag
            if stripped in ["@ul", "@ol"]:
                i += 1
                break
            # Stop at next widget or slide
            if stripped.startswith("@") and not stripped.startswith("-"):
                break
            if stripped == "---" or stripped.startswith("["):
                break

            # Parse list item
            if stripped.startswith("- ") or stripped.startswith("* "):
                items.append(stripped[2:])
            elif re.match(r"^\d+\.\s", stripped):
                items.append(re.sub(r"^\d+\.\s", "", stripped))

            i += 1

        node = PitchListNode()
        node["list_type"] = list_type
        node["classes"] = classes
        node["items"] = items
        parent += node

        return i

    def _parse_math_widget(self, parent, lines, start_idx):
        """Parse @math widget."""
        header = lines[start_idx].strip()
        match = re.match(r"@math\[([^\]]*)\]", header)
        attrs = {}

        if match:
            for part in match.group(1).split(","):
                if "=" in part:
                    k, v = part.split("=", 1)
                    attrs[k.strip()] = v.strip()

        # Collect math content
        content_lines = []
        i = start_idx + 1
        while i < len(lines):
            line = lines[i]
            if line.strip() == "@math":
                i += 1
                break
            content_lines.append(line)
            i += 1

        # For now, render math as preformatted text
        node = PitchCodeNode()
        node["attrs"] = {"language": "math"}
        node["content"] = "\n".join(content_lines)
        parent += node

        return i

    def _parse_note(self, parent, lines, start_idx):
        """Parse Note: speaker notes."""
        i = start_idx + 1
        note_lines = []

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                i += 1
                break
            if (
                stripped.startswith("@")
                or stripped.startswith("[")
                or stripped == "---"
            ):
                break

            note_lines.append(line)
            i += 1

        node = PitchNoteNode()
        node["content"] = "\n".join(note_lines)
        parent += node

        return i

    def _parse_float_block(self, parent, lines, start_idx):
        """Parse [drag=..., drop=...] grid block."""
        header = lines[start_idx].strip()
        attrs = {}

        # Parse attributes
        for match in re.finditer(r"(\w+)=([^,\]]+)", header):
            attrs[match.group(1)] = match.group(2).strip()

        # Collect content until next block or widget
        content_lines = []
        i = start_idx + 1
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if stripped.startswith("[") and "drag=" in stripped:
                break
            if stripped.startswith("@") or stripped == "---":
                break

            content_lines.append(line)
            i += 1

        node = PitchFloatNode()
        node["attrs"] = attrs

        # Parse content inside the block
        for line in content_lines:
            stripped = line.strip()
            if stripped:
                self._add_content(node, stripped)

        parent += node
        return i

    def _add_content(self, parent, line):
        """Add regular content (headings, paragraphs)."""
        if line.startswith("# "):
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-1"]
            strong = nodes.strong()
            strong += nodes.Text(line[2:])
            para += strong
            parent += para
        elif line.startswith("## "):
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-2"]
            strong = nodes.strong()
            strong += nodes.Text(line[3:])
            para += strong
            parent += para
        elif line.startswith("- ") or line.startswith("* "):
            para = nodes.paragraph()
            para += nodes.Text("• " + line[2:])
            parent += para
        else:
            para = nodes.paragraph()
            para += nodes.Text(line)
            parent += para


def setup(app: Sphinx):
    app.add_directive("pitch", PitchDirective)

    app.add_node(
        PitchNode,
        html=(visit_pitch_node, depart_pitch_node),
        latex=(visit_pitch_node, depart_pitch_node),
        text=(visit_pitch_node, depart_pitch_node),
    )

    app.add_node(
        PitchSlideNode,
        html=(visit_pitch_slide_node, depart_pitch_slide_node),
        latex=(visit_pitch_slide_node, depart_pitch_slide_node),
        text=(visit_pitch_slide_node, depart_pitch_slide_node),
    )

    app.add_node(
        PitchFloatNode,
        html=(visit_pitch_float_node, depart_pitch_float_node),
        latex=(visit_pitch_float_node, depart_pitch_float_node),
        text=(visit_pitch_float_node, depart_pitch_float_node),
    )

    app.add_node(
        PitchCodeNode,
        html=(visit_pitch_code_node, depart_pitch_code_node),
        latex=(visit_pitch_code_node, depart_pitch_code_node),
        text=(visit_pitch_code_node, depart_pitch_code_node),
    )

    app.add_node(
        PitchListNode,
        html=(visit_pitch_list_node, depart_pitch_list_node),
        latex=(visit_pitch_list_node, depart_pitch_list_node),
        text=(visit_pitch_list_node, depart_pitch_list_node),
    )

    app.add_node(
        PitchNoteNode,
        html=(visit_pitch_note_node, depart_pitch_note_node),
        latex=(visit_pitch_note_node, depart_pitch_note_node),
        text=(visit_pitch_note_node, depart_pitch_note_node),
    )

    app.add_css_file("pitch.css")
    app.add_config_value("pitch_theme", "default", "html")
    app.add_config_value("pitch_transition", "slide", "html")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
