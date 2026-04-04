"""
sphinx-pitch: A Sphinx extension for creating presentations like GitPitch.

This extension provides directives compatible with GitPitch markdown syntax
for creating slide presentations using sphinx-revealjs.
"""

import re
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class PitchNode(nodes.General, nodes.Element):
    """Node representing a pitch/presentation container."""

    pass


class PitchSlideNode(nodes.General, nodes.Element):
    """Node representing an individual slide section."""

    pass


class PitchFloatNode(nodes.General, nodes.Element):
    """Node representing a positioned floating block (GitPitch grid layout)."""

    pass


class PitchCodeNode(nodes.General, nodes.Element):
    """Node representing a code block widget."""

    pass


class PitchListNode(nodes.General, nodes.Element):
    """Node representing a list widget (@ul or @ol)."""

    pass


class PitchMathNode(nodes.General, nodes.Element):
    """Node representing a math formula widget."""

    pass


class PitchNoteNode(nodes.General, nodes.Element):
    """Node representing speaker notes."""

    pass


# Visitor functions for HTML output (standard Sphinx HTML)
def visit_pitch_node(self, node):
    self.body.append('<div class="pitch-presentation">')
    self.body.append('<div class="pitch-slides">')


def depart_pitch_node(self, node):
    self.body.append("</div>")  # Close pitch-slides

    # Add navigation controls with JavaScript
    self.body.append("""
<div class="pitch-controls">
    <button class="pitch-prev" onclick="pitchNavigate(-1)">← Previous</button>
    <span class="pitch-slide-number">1 / 1</span>
    <button class="pitch-next" onclick="pitchNavigate(1)">Next →</button>
</div>
<script>
(function() {
    const presentation = document.currentScript.closest('.pitch-presentation');
    const slides = presentation.querySelectorAll('.pitch-slide');
    const slideNumber = presentation.querySelector('.pitch-slide-number');
    const prevBtn = presentation.querySelector('.pitch-prev');
    const nextBtn = presentation.querySelector('.pitch-next');
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    function updateSlides() {
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentSlide);
        });
        if (slideNumber) {
            slideNumber.textContent = (currentSlide + 1) + ' / ' + totalSlides;
        }
        if (prevBtn) prevBtn.disabled = currentSlide === 0;
        if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;
    }
    
    window.pitchNavigate = function(direction) {
        const newSlide = currentSlide + direction;
        if (newSlide >= 0 && newSlide < totalSlides) {
            currentSlide = newSlide;
            updateSlides();
        }
    };
    
    document.addEventListener('keydown', function(e) {
        const isPresentationVisible = presentation.getBoundingClientRect().top < window.innerHeight && 
                                     presentation.getBoundingClientRect().bottom > 0;
        if (!isPresentationVisible) return;
        
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            pitchNavigate(-1);
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
            e.preventDefault();
            pitchNavigate(1);
        }
    });
    
    updateSlides();
})();
</script>
</div>""")


def visit_pitch_slide_node(self, node):
    slide_id = node.get("slide_id", "")
    self.body.append(f'<section class="pitch-slide" id="{slide_id}">')


def depart_pitch_slide_node(self, node):
    self.body.append("</section>")


def visit_pitch_float_node(self, node):
    """Output GitPitch-style grid layout block."""
    attrs = node.get("attrs", {})

    styles = ["position: absolute;"]
    classes = ["pitch-grid-block"]

    # Parse drag (width height)
    drag = attrs.get("drag", "")
    if drag:
        parts = drag.split()
        if len(parts) >= 1:
            w = parts[0]
            styles.append(f"width: {w}{'%' if w.isdigit() else ''};")
        if len(parts) >= 2:
            h = parts[1]
            styles.append(f"height: {h}{'%' if h.isdigit() else ''};")

    # Parse drop (position)
    drop = attrs.get("drop", "")
    if drop:
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
        else:
            parts = drop.split()
            if len(parts) >= 1:
                x = parts[0]
                styles.append(f"left: {x}{'%' if x.isdigit() else ''};")
            if len(parts) >= 2:
                y = parts[1]
                styles.append(f"top: {y}{'%' if y.isdigit() else ''};")

    fit = attrs.get("fit", "")
    if fit:
        styles.append(f"--pitch-fit: {fit};")

    bg = attrs.get("bg", "")
    if bg:
        styles.append(f"background-color: {bg};")

    flow = attrs.get("flow", "")
    if flow:
        classes.append(f"flow-{flow}")

    style_attr = " ".join(styles)
    class_attr = " ".join(classes)

    self.body.append(f'<div class="{class_attr}" style="{style_attr}">')


def depart_pitch_float_node(self, node):
    self.body.append("</div>")


def visit_pitch_code_node(self, node):
    import html as html_module

    attrs = node.get("attrs", {})
    language = attrs.get("language", "text")
    content = node.get("content", "")

    escaped = html_module.escape(content)
    self.body.append(
        f'<div class="pitch-code-widget"><pre><code class="language-{language}">{escaped}</code></pre></div>'
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

    items = node.get("items", [])
    for item in items:
        self.body.append(f"<li>{item}</li>")


def depart_pitch_list_node(self, node):
    list_type = node.get("list_type", "ul")
    if list_type == "ol":
        self.body.append("</ol>")
    else:
        self.body.append("</ul>")


def visit_pitch_math_node(self, node):
    self.body.append('<div class="pitch-math-widget">')
    content = node.get("content", "")
    if content:
        self.body.append(content)


def depart_pitch_math_node(self, node):
    self.body.append("</div>")


def visit_pitch_note_node(self, node):
    self.body.append('<aside class="pitch-notes" style="display: none;">')
    content = node.get("content", "")
    if content:
        self.body.append(content)


def depart_pitch_note_node(self, node):
    self.body.append("</aside>")


class PitchDirective(SphinxDirective):
    """
    Main directive for creating pitch presentations.

    Uses GitPitch-style syntax:
    - Slide delimiters: ---
    - Grid layouts: [drag=X, drop=Y, fit=Z, bg=COLOR]
    - Code widgets: @code[LANGUAGE]
    - List widgets: @ul/@ol
    - Math widgets: @math
    - Speaker notes: Note:
    """

    has_content = True
    option_spec = {
        "theme": directives.unchanged,
        "transition": directives.unchanged,
    }

    def run(self):
        pitch_node = PitchNode()
        pitch_node["options"] = self.options

        # Split content by slide delimiter
        content = "\n".join(self.content)
        slides = re.split(r"\n---\s*\n", content)

        for i, slide_content in enumerate(slides):
            slide_content = slide_content.strip()
            if not slide_content:
                continue

            slide_node = PitchSlideNode()
            slide_node["slide_id"] = f"slide-{i + 1}"

            # Parse slide content
            self._parse_slide_content(slide_node, slide_content)

            pitch_node += slide_node

        return [pitch_node]

    def _parse_slide_content(self, slide_node, content):
        """Parse slide content and create child nodes."""
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Grid layout block: [drag=..., drop=...]
            if stripped.startswith("[") and "drag=" in stripped:
                block_data, i = self._extract_float_block(lines, i)
                float_node = self._create_float_node(block_data)
                slide_node += float_node

            # Code widget: @code[LANGUAGE]
            elif stripped.startswith("@code["):
                code_data, i = self._extract_code_widget(lines, i)
                code_node = self._create_code_node(code_data)
                slide_node += code_node

            # List widget: @ul or @ol
            elif stripped.startswith("@ul") or stripped.startswith("@ol"):
                list_data, i = self._extract_list_widget(lines, i)
                list_node = self._create_list_node(list_data)
                slide_node += list_node

            # Math widget: @math
            elif stripped.startswith("@math"):
                math_data, i = self._extract_math_widget(lines, i)
                math_node = self._create_math_node(math_data)
                slide_node += math_node

            # Speaker notes: Note:
            elif stripped.startswith("Note:"):
                note_data, i = self._extract_note(lines, i)
                note_node = self._create_note_node(note_data)
                slide_node += note_node

            # Regular content (headings, paragraphs)
            else:
                if stripped:
                    self._add_regular_content(slide_node, stripped)
                i += 1

    def _extract_float_block(self, lines, start_idx):
        """Extract grid layout block content."""
        header = lines[start_idx]
        attrs = self._parse_attrs(header)

        content_lines = []
        i = start_idx + 1

        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("[") and "drag=" in line:
                break
            if line.strip() == "---":
                break
            content_lines.append(line)
            i += 1

        return {"attrs": attrs, "content": "\n".join(content_lines)}, i

    def _create_float_node(self, data):
        """Create a float/grid block node."""
        node = PitchFloatNode()
        node["attrs"] = data["attrs"]

        # Parse the content as nested RST
        content = data["content"]
        if content:
            # Parse content for headings, lists, etc.
            lines = content.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                self._add_regular_content(node, line)

        return node

    def _extract_code_widget(self, lines, start_idx):
        """Extract @code widget content."""
        header = lines[start_idx]
        match = re.match(r"@code\[([^\]]*)\]", header)
        attrs = {}

        if match:
            attr_str = match.group(1)
            parts = [p.strip() for p in attr_str.split(",")]
            if parts and parts[0] and "=" not in parts[0]:
                attrs["language"] = parts[0]
            for part in parts[1:] if len(parts) > 1 else parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    attrs[k.strip()] = v.strip()

        content_lines = []
        i = start_idx + 1

        # Collect until empty line or next special element
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
            if stripped.startswith("Note:"):
                break
            content_lines.append(line)
            i += 1

        return {"attrs": attrs, "content": "\n".join(content_lines)}, i

    def _create_code_node(self, data):
        """Create a code widget node."""
        node = PitchCodeNode()
        node["attrs"] = data["attrs"]
        node["content"] = data["content"]
        return node

    def _extract_list_widget(self, lines, start_idx):
        """Extract @ul or @ol widget content."""
        header = lines[start_idx]
        list_type = "ol" if header.strip().startswith("@ol") else "ul"

        # Parse classes from header
        match = re.match(r"@(?:ul|ol)\[([^\]]*)\]", header)
        classes = []
        if match:
            classes = [
                c.strip()
                for c in match.group(1).split(",")
                if c.strip() and "=" not in c.strip()
            ]

        content_lines = []
        i = start_idx + 1

        # Collect until closing tag @ul/@ol
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if stripped in ["@ul", "@ol"]:
                i += 1
                break
            if stripped.startswith("@") and not stripped.startswith("-"):
                break
            if stripped == "---":
                break
            content_lines.append(line)
            i += 1

        return {"type": list_type, "classes": classes, "lines": content_lines}, i

    def _create_list_node(self, data):
        """Create a list widget node."""
        node = PitchListNode()
        node["list_type"] = data["type"]
        node["classes"] = data["classes"]

        # Parse list items
        items = []
        for line in data["lines"]:
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                items.append(stripped[2:])
            elif re.match(r"^\d+\.\s", stripped):
                items.append(re.sub(r"^\d+\.\s", "", stripped))

        node["items"] = items
        return node

    def _extract_math_widget(self, lines, start_idx):
        """Extract @math widget content."""
        header = lines[start_idx]
        match = re.match(r"@math\[([^\]]*)\]", header)
        attrs = {}

        if match:
            for part in match.group(1).split(","):
                if "=" in part:
                    k, v = part.split("=", 1)
                    attrs[k.strip()] = v.strip()

        content_lines = []
        i = start_idx + 1

        # Collect until closing @math
        while i < len(lines):
            line = lines[i]
            if line.strip() == "@math":
                i += 1
                break
            content_lines.append(line)
            i += 1

        return {"attrs": attrs, "content": "\n".join(content_lines)}, i

    def _create_math_node(self, data):
        """Create a math widget node."""
        node = PitchMathNode()
        node["attrs"] = data["attrs"]
        node["content"] = data["content"]
        return node

    def _extract_note(self, lines, start_idx):
        """Extract speaker notes."""
        i = start_idx + 1
        content_lines = []

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                i += 1
                break
            if (
                stripped.startswith("[")
                or stripped.startswith("@")
                or stripped == "---"
            ):
                break
            content_lines.append(line)
            i += 1

        return {"content": "\n".join(content_lines)}, i

    def _create_note_node(self, data):
        """Create a speaker note node."""
        node = PitchNoteNode()
        node["content"] = data["content"]
        return node

    def _parse_attrs(self, line):
        """Parse attributes like [drag=50, drop=center, fit=2]."""
        attrs = {}
        content = line.strip()
        if content.startswith("[") and content.endswith("]"):
            content = content[1:-1]

        for match in re.finditer(r"(\w+)=([^,\]]+)", content):
            attrs[match.group(1)] = match.group(2).strip()

        return attrs

    def _add_regular_content(self, parent, line):
        """Add regular content (headings, paragraphs) as nodes."""
        # Heading 1: # Title
        if line.startswith("# "):
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-1"]
            strong = nodes.strong()
            strong += nodes.Text(line[2:])
            para += strong
            parent += para

        # Heading 2: ## Subtitle
        elif line.startswith("## "):
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-2"]
            strong = nodes.strong()
            strong += nodes.Text(line[3:])
            para += strong
            parent += para

        # List item (inline)
        elif line.startswith("- ") or line.startswith("* "):
            para = nodes.paragraph()
            para += nodes.Text("• " + line[2:])
            parent += para

        # Regular paragraph
        else:
            para = nodes.paragraph()
            para += nodes.Text(line)
            parent += para


def setup(app: Sphinx):
    """Setup the sphinx-pitch extension."""

    # Add directive
    app.add_directive("pitch", PitchDirective)

    # Add nodes with visitor functions
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
        PitchMathNode,
        html=(visit_pitch_math_node, depart_pitch_math_node),
        latex=(visit_pitch_math_node, depart_pitch_math_node),
        text=(visit_pitch_math_node, depart_pitch_math_node),
    )

    app.add_node(
        PitchNoteNode,
        html=(visit_pitch_note_node, depart_pitch_note_node),
        latex=(visit_pitch_note_node, depart_pitch_note_node),
        text=(visit_pitch_note_node, depart_pitch_note_node),
    )

    # Add CSS
    app.add_css_file("pitch.css")

    # Config values
    app.add_config_value("pitch_theme", "default", "html")
    app.add_config_value("pitch_transition", "slide", "html")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
