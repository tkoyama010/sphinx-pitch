"""
sphinx-pitch: A Sphinx extension for creating presentations like GitPitch.

This extension provides directives and roles compatible with GitPitch markdown syntax.
GitPitch uses PITCHME.md files with special syntax for creating slide presentations.

Main features:
- pitch directive: Main container for slide presentations
- Support for GitPitch grid layout syntax [drag=X, drop=Y, fit=Z]
- Support for GitPitch widgets (@code, @ul, @ol, @math, @gist, @diff, @mermaid)
- Slide delimiter support (---)
- Code presenting with annotations
- Speaker notes
"""

import html
import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import ViewList
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class PitchNode(nodes.General, nodes.Element):
    """Node representing a pitch/presentation slide deck."""

    pass


class SlideNode(nodes.General, nodes.Element):
    """Node representing an individual slide."""

    pass


class GridBlockNode(nodes.General, nodes.Element):
    """Node representing a grid layout block with drag/drop positioning."""

    pass


class CodeWidgetNode(nodes.General, nodes.Element):
    """Node representing a @code widget."""

    pass


class ListWidgetNode(nodes.General, nodes.Element):
    """Node representing @ul or @ol widget."""

    pass


class MathWidgetNode(nodes.General, nodes.Element):
    """Node representing @math widget."""

    pass


class NoteNode(nodes.General, nodes.Element):
    """Node representing speaker notes."""

    pass


def visit_pitch_node(self, node):
    """Generate HTML output for pitch node with slideshow container."""
    self.body.append('<div class="pitch-presentation">')
    self.body.append('<div class="pitch-slides-container">')


def depart_pitch_node(self, node):
    """Close pitch node and add navigation controls."""
    self.body.append("</div>")  # Close slides container

    # Add navigation controls
    self.body.append("""
<div class="pitch-nav">
    <button class="pitch-prev" onclick="pitchPrevSlide(this)">← Previous</button>
    <span class="pitch-slide-counter"><span class="pitch-current">1</span> / <span class="pitch-total">1</span></span>
    <button class="pitch-next" onclick="pitchNextSlide(this)">Next →</button>
</div>
<script>
(function() {
    function initPitchPresentation(container) {
        const slides = container.querySelectorAll('.pitch-slide');
        const totalSlides = slides.length;
        let currentSlide = 0;
        
        if (totalSlides === 0) return;
        
        // Show first slide
        slides[0].classList.add('active');
        
        // Update counter
        const counter = container.parentElement.querySelector('.pitch-slide-counter');
        if (counter) {
            counter.querySelector('.pitch-total').textContent = totalSlides;
            updateCounter();
        }
        
        function updateCounter() {
            if (counter) {
                counter.querySelector('.pitch-current').textContent = currentSlide + 1;
            }
            const prevBtn = container.parentElement.querySelector('.pitch-prev');
            const nextBtn = container.parentElement.querySelector('.pitch-next');
            if (prevBtn) prevBtn.disabled = currentSlide === 0;
            if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;
        }
        
        window.pitchNextSlide = function(btn) {
            if (currentSlide < totalSlides - 1) {
                slides[currentSlide].classList.remove('active');
                currentSlide++;
                slides[currentSlide].classList.add('active');
                updateCounter();
            }
        };
        
        window.pitchPrevSlide = function(btn) {
            if (currentSlide > 0) {
                slides[currentSlide].classList.remove('active');
                currentSlide--;
                slides[currentSlide].classList.add('active');
                updateCounter();
            }
        };
    }
    
    // Initialize all presentations
    document.querySelectorAll('.pitch-slides-container').forEach(initPitchPresentation);
})();
</script>
''')
    self.body.append("</div>")  # Close presentation


def visit_slide_node(self, node):
    """Generate HTML output for slide node."""
    slide_id = node.get("slide_id", "")
    classes = ["pitch-slide"]
    if node.get("classes"):
        classes.extend(node.get("classes"))

    class_attr = " ".join(classes)
    self.body.append(f'<section class="{class_attr}" id="{slide_id}">')


def depart_slide_node(self, node):
    self.body.append("</section>")


def visit_grid_block_node(self, node):
    """Generate HTML output for grid block node with GitPitch-style positioning."""
    drag = node.get("drag", "")
    drop = node.get("drop", "")
    fit = node.get("fit", "")
    flow = node.get("flow", "")
    bg = node.get("bg", "")

    styles = ["position: absolute;"]
    classes = ["pitch-grid-block"]

    # Parse drag (width height)
    if drag:
        drag_parts = drag.split()
        if len(drag_parts) >= 1:
            styles.append(f"width: {drag_parts[0]};")
        if len(drag_parts) >= 2:
            styles.append(f"height: {drag_parts[1]};")

    # Parse drop (x y or named position)
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
            drop_parts = drop.split()
            if len(drop_parts) >= 1:
                styles.append(f"left: {drop_parts[0]};")
            if len(drop_parts) >= 2:
                styles.append(f"top: {drop_parts[1]};")

    if fit:
        styles.append(f"--pitch-fit: {fit};")

    if bg:
        styles.append(f"background-color: {bg};")

    if flow:
        classes.append(f"flow-{flow}")

    style_attr = " ".join(styles)
    class_attr = " ".join(classes)

    self.body.append(f'<div class="{class_attr}" style="{style_attr}">')


def depart_grid_block_node(self, node):
    self.body.append("</div>")


def visit_note_node(self, node):
    """Generate HTML output for speaker notes."""
    self.body.append('<aside class="pitch-notes" style="display: none;">')


def depart_note_node(self, node):
    self.body.append("</aside>")


def visit_code_widget_node(self, node):
    """Generate HTML output for code widget."""
    attrs = node.get("attrs", {})
    language = attrs.get("language", "text")
    content = node.get("content", "")
    
    # Escape HTML in code content
    import html
    escaped_content = html.escape(content)
    
    self.body.append(
        f'<div class="pitch-code-widget" data-language="{language}"><pre><code class="language-{language}">'
    )
    if escaped_content:
        self.body.append(escaped_content)


def depart_code_widget_node(self, node):
    self.body.append("</code></pre></div>")


def visit_list_widget_node(self, node):
    """Generate HTML output for list widget."""
    list_type = node.get("list_type", "ul")
    classes = node.get("classes", [])
    class_attr = " ".join(classes)

    if list_type == "ol":
        self.body.append(f'<ol class="pitch-list-widget {class_attr}">')
    else:
        self.body.append(f'<ul class="pitch-list-widget {class_attr}">')


def depart_list_widget_node(self, node):
    list_type = node.get("list_type", "ul")
    if list_type == "ol":
        self.body.append("</ol>")
    else:
        self.body.append("</ul>")


def visit_math_widget_node(self, node):
    """Generate HTML output for math widget."""
    self.body.append('<div class="pitch-math-widget">')


def depart_math_widget_node(self, node):
    self.body.append("</div>")


class PitchDirective(SphinxDirective):
    """
    Main directive for creating pitch presentations.

    This directive processes GitPitch-style markdown syntax including:
    - Slide delimiters (---)
    - Grid layout blocks [drag=X, drop=Y, fit=Z]
    - Widgets (@code, @ul, @ol, @math)
    - Speaker notes (Note:)
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True

    option_spec = {
        "theme": directives.unchanged,
        "transition": directives.unchanged,
        "background": directives.unchanged,
        "height": directives.unchanged,
        "width": directives.unchanged,
    }

    def run(self):
        """Process the pitch directive content."""
        pitch_node = PitchNode()
        pitch_node["options"] = self.options

        # Join content lines
        content = "\n".join(self.content)

        # Parse GitPitch-style syntax
        self._parse_slides(pitch_node, content)

        return [pitch_node]

    def _parse_slides(self, parent_node, content):
        """Parse content and split into slides."""
        # Split by slide delimiter (---)
        slides = re.split(r"\n---\s*\n", content)

        for i, slide_content in enumerate(slides):
            slide_content = slide_content.strip()
            if not slide_content:
                continue

            slide_node = SlideNode()
            slide_node["slide_id"] = f"slide-{i + 1}"

            # Parse slide content for grid blocks, widgets, etc.
            self._parse_slide_content(slide_node, slide_content)

            parent_node += slide_node

    def _parse_slide_content(self, slide_node, content):
        """Parse individual slide content."""
        lines = content.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]

            # Check for grid block start [drag=X, drop=Y, ...]
            if line.strip().startswith("[") and "drag=" in line:
                block_content, i = self._extract_grid_block(lines, i)
                grid_node = self._create_grid_block(block_content)
                slide_node += grid_node
            # Check for @code widget
            elif line.strip().startswith("@code["):
                code_lines, i = self._extract_code_widget(lines, i)
                code_node = self._create_code_widget(code_lines)
                slide_node += code_node
            # Check for @ul/@ol widget
            elif line.strip().startswith("@ul") or line.strip().startswith("@ol"):
                list_content, list_type, i = self._extract_list_widget(lines, i)
                list_node = self._create_list_widget(list_content, list_type)
                slide_node += list_node
            # Check for @math widget
            elif line.strip().startswith("@math"):
                math_content, i = self._extract_math_widget(lines, i)
                math_node = self._create_math_widget(math_content)
                slide_node += math_node
            # Check for Note: (speaker notes)
            elif line.strip().startswith("Note:"):
                note_content, i = self._extract_note(lines, i)
                note_node = self._create_note(note_content)
                slide_node += note_node
            else:
                # Regular content - parse as rst
                if line.strip():
                    self._parse_regular_content(slide_node, line)
                i += 1

    def _extract_grid_block(self, lines, start_idx):
        """Extract grid block content."""
        header_line = lines[start_idx]

        # Parse grid attributes from header
        attrs = self._parse_grid_attributes(header_line)

        content_lines = []
        i = start_idx + 1

        # Collect content until next grid block or end
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("[") and "drag=" in line:
                break
            if line.strip().startswith("---"):
                break
            content_lines.append(line)
            i += 1

        return {"attrs": attrs, "content": "\n".join(content_lines)}, i

    def _parse_grid_attributes(self, line):
        """Parse grid attributes like [drag=50, drop=center, fit=2]."""
        attrs = {}

        # Remove brackets
        content = line.strip()[1:-1] if line.strip().endswith("]") else line.strip()[1:]

        # Parse key=value pairs
        pairs = re.findall(r"(\w+)=([^,\]]+)", content)
        for key, value in pairs:
            attrs[key] = value.strip()

        return attrs

    def _create_grid_block(self, block_data):
        """Create a grid block node from parsed data."""
        grid_node = GridBlockNode()
        attrs = block_data["attrs"]

        grid_node["drag"] = attrs.get("drag", "")
        grid_node["drop"] = attrs.get("drop", "")
        grid_node["fit"] = attrs.get("fit", "")
        grid_node["flow"] = attrs.get("flow", "")
        grid_node["bg"] = attrs.get("bg", "")

        # Parse content inside grid block
        content = block_data["content"]
        self._parse_slide_content(grid_node, content)

        return grid_node

    def _extract_code_widget(self, lines, start_idx):
        """Extract @code widget content (inline or file reference)."""
        header_line = lines[start_idx]
        
        # Parse attributes from header
        match = re.match(r'@code\[([^\]]*)\]', header_line)
        attrs = {}
        file_path = None
        
        if match:
            attr_str = match.group(1)
            # Check if there's a file path: @code[attrs](path)
            path_match = re.search(r'\]\(([^)]+)\)', header_line)
            if path_match:
                file_path = path_match.group(1)
            
            # Parse attributes
            for pair in attr_str.split(','):
                pair = pair.strip()
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    attrs[key.strip()] = value.strip()
                elif pair and not file_path:
                    # First non-key-value is language
                    attrs['language'] = pair
        
        content_lines = []
        i = start_idx + 1
        
        if file_path:
            # External file reference - no inline content
            attrs['path'] = file_path
        else:
            # Inline code - collect until next special element or empty line
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    i += 1
                    break
                if line.strip().startswith('@') or line.strip().startswith('[') or line.strip().startswith('---'):
                    break
                if line.strip().startswith('Note:'):
                    break
                content_lines.append(line)
                i += 1
        
        return {'attrs': attrs, 'content': '\n'.join(content_lines)}, i

    def _create_code_widget(self, data):
        """Create a code widget node from parsed data."""
        node = CodeWidgetNode()
        node['attrs'] = data['attrs']
        node['content'] = data['content']
        
        # Add code content as text node
        if data['content']:
            text_node = nodes.literal_block(text=data['content'])
            text_node['language'] = data['attrs'].get('language', 'text')
            node += text_node
        
        return node

    def _parse_code_widget_old(self, line):
        """Parse @code[language](path) syntax."""
        node = CodeWidgetNode()

        # Extract language and file path
        match = re.match(r"@code\[([^\]]+)\]\(([^)]+)\)", line.strip())
        if match:
            params = match.group(1).split(",")
            node["language"] = params[0].strip()
            node["path"] = match.group(2)

            # Parse additional attributes
            for param in params[1:]:
                param = param.strip()
                if "drag=" in param:
                    node["drag"] = param.replace("drag=", "")
                elif "drop=" in param:
                    node["drop"] = param.replace("drop=", "")
                elif "fit=" in param:
                    node["fit"] = param.replace("fit=", "")

        return node

    def _extract_list_widget(self, lines, start_idx):
        """Extract @ul or @ol widget content."""
        header_line = lines[start_idx]

        # Determine list type
        list_type = "ol" if header_line.strip().startswith("@ol") else "ul"

        # Parse attributes from header
        attrs_match = re.match(r"@(?:ul|ol)\[([^\]]*)\]", header_line)
        classes = []
        if attrs_match:
            classes = [c.strip() for c in attrs_match.group(1).split(",") if c.strip()]

        content_lines = []
        i = start_idx + 1

        # Collect until closing tag
        while i < len(lines):
            line = lines[i]
            if line.strip() in ["@ul", "@ol"]:
                i += 1
                break
            if line.strip().startswith("@") and not line.strip().startswith("-"):
                break
            content_lines.append(line)
            i += 1

        return content_lines, list_type, i

    def _create_list_widget(self, content_lines, list_type):
        """Create a list widget node."""
        node = ListWidgetNode()
        node["list_type"] = list_type
        node["classes"] = []

        # Parse list items
        for line in content_lines:
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                # Create list item node with paragraph
                item_node = nodes.list_item()
                para = nodes.paragraph()
                para += nodes.Text(line[2:])
                item_node += para
                node += item_node
            elif re.match(r"^\d+\.\s", line):
                # Ordered list item
                item_node = nodes.list_item()
                para = nodes.paragraph()
                text = re.sub(r"^\d+\.\s", "", line)
                para += nodes.Text(text)
                item_node += para
                node += item_node

        return node

    def _extract_math_widget(self, lines, start_idx):
        """Extract @math widget content."""
        header_line = lines[start_idx]

        # Parse attributes
        attrs_match = re.match(r"@math\[([^\]]*)\]", header_line)
        attrs = {}
        if attrs_match:
            attr_str = attrs_match.group(1)
            for pair in attr_str.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    attrs[key.strip()] = value.strip()

        content_lines = []
        i = start_idx + 1

        # Collect until closing @math tag
        while i < len(lines):
            line = lines[i]
            if line.strip() == "@math":
                i += 1
                break
            content_lines.append(line)
            i += 1

        return {"attrs": attrs, "content": "\n".join(content_lines)}, i

    def _create_math_widget(self, data):
        """Create a math widget node."""
        node = MathWidgetNode()
        node["attrs"] = data["attrs"]
        node["content"] = data["content"]
        return node

    def _extract_note(self, lines, start_idx):
        """Extract speaker notes."""
        # Skip "Note:" line
        i = start_idx + 1
        content_lines = []

        # Collect all following lines until empty line or next special element
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                break
            if line.strip().startswith("[") or line.strip().startswith("@"):
                break
            content_lines.append(line)
            i += 1

        return "\n".join(content_lines), i

    def _create_note(self, content):
        """Create a speaker note node."""
        node = NoteNode()
        node["content"] = content
        return node

    def _parse_regular_content(self, parent, line):
        """Parse regular markdown/rst content."""
        # Handle markdown headers - use strong paragraph instead of title
        # (title nodes must be children of section nodes)
        if line.startswith("# "):
            title = line[2:]
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-1"]
            strong = nodes.strong()
            strong += nodes.Text(title)
            para += strong
            parent += para
        elif line.startswith("## "):
            title = line[3:]
            para = nodes.paragraph()
            para["classes"] = ["pitch-heading-2"]
            strong = nodes.strong()
            strong += nodes.Text(title)
            para += strong
            parent += para
        else:
            # Regular paragraph
            para = nodes.paragraph()
            para += nodes.Text(line)
            parent += para


def setup(app: Sphinx):
    """Setup the sphinx-pitch extension."""

    # Add the pitch directive
    app.add_directive("pitch", PitchDirective)

    # Add custom nodes
    app.add_node(
        PitchNode,
        html=(visit_pitch_node, depart_pitch_node),
        latex=(visit_pitch_node, depart_pitch_node),
        text=(visit_pitch_node, depart_pitch_node),
    )

    app.add_node(
        SlideNode,
        html=(visit_slide_node, depart_slide_node),
        latex=(visit_slide_node, depart_slide_node),
        text=(visit_slide_node, depart_slide_node),
    )

    app.add_node(
        GridBlockNode,
        html=(visit_grid_block_node, depart_grid_block_node),
        latex=(visit_grid_block_node, depart_grid_block_node),
        text=(visit_grid_block_node, depart_grid_block_node),
    )

    app.add_node(
        CodeWidgetNode,
        html=(visit_code_widget_node, depart_code_widget_node),
        latex=(visit_code_widget_node, depart_code_widget_node),
        text=(visit_code_widget_node, depart_code_widget_node),
    )

    app.add_node(
        ListWidgetNode,
        html=(visit_list_widget_node, depart_list_widget_node),
        latex=(visit_list_widget_node, depart_list_widget_node),
        text=(visit_list_widget_node, depart_list_widget_node),
    )

    app.add_node(
        MathWidgetNode,
        html=(visit_math_widget_node, depart_math_widget_node),
        latex=(visit_math_widget_node, depart_math_widget_node),
        text=(visit_math_widget_node, depart_math_widget_node),
    )

    app.add_node(
        NoteNode,
        html=(visit_note_node, depart_note_node),
        latex=(visit_note_node, depart_note_node),
        text=(visit_note_node, depart_note_node),
    )

    # Add CSS file
    app.add_css_file("pitch.css")

    # Add configuration values
    app.add_config_value("pitch_theme", "default", "html")
    app.add_config_value("pitch_transition", "slide", "html")

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
