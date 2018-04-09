import sublime
import sublime_plugin
import datetime, getpass
import re

# Sublime Text API Reference: https://www.sublimetext.com/docs/3/api_reference.html

_figlet_letters = {
    "A" : [
        " █████╗ ",
        "██╔══██╗",
        "███████║",
        "██╔══██║",
        "██║  ██║",
        "╚═╝  ╚═╝"
    ],
    "B" : [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔══██╗",
        "██████╔╝",
        "╚═════╝ "
    ],
    "C" : [
        " █████╗",
        "██╔═══╝",
        "██║    ",
        "██║    ",
        "╚█████╗",
        " ╚════╝"
    ],
    "D" : [
        "█████╗ ",
        "██╔═██╗",
        "██║ ██║",
        "██║ ██║",
        "█████╔╝",
        "╚════╝ "
    ],
    "E" : [
        "██████╗",
        "██╔═══╝",
        "████╗  ",
        "██╔═╝  ",
        "██████╗",
        "╚═════╝"
    ],
    "F" : [
        "██████╗",
        "██╔═══╝",
        "████╗  ",
        "██╔═╝  ",
        "██║    ",
        "╚═╝    "
    ],
    "G" : [
        " █████╗ ",
        "██╔═══╝ ",
        "██║ ███╗",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "H" : [
        "██╗ ██╗",
        "██║ ██║",
        "██████║",
        "██╔═██║",
        "██║ ██║",
        "╚═╝ ╚═╝"
    ],
    "I" : [
        "██╗",
        "██║",
        "██║",
        "██║",
        "██║",
        "╚═╝"
    ],
    "J" : [
        "    ██╗",
        "    ██║",
        "    ██║",
        "██  ██║",
        "╚████╔╝",
        " ╚═══╝ "
    ],
    "K" : [
        "██╗  ██╗",
        "██║ ██╔╝",
        "█████╔╝ ",
        "██╔═██╗ ",
        "██║  ██╗",
        "╚═╝  ╚═╝"
    ],
    "L" : [
        "██╗    ",
        "██║    ",
        "██║    ",
        "██║    ",
        "██████╗",
        "╚═════╝"
    ],
    "M" : [
        "███╗   ███╗",
        "████╗ ████║",
        "██╔████╔██║",
        "██║╚██╔╝██║",
        "██║ ╚═╝ ██║",
        "╚═╝     ╚═╝"
    ],
    "N" : [
        "███╗   ██╗",
        "████╗  ██║",
        "██╔██╗ ██║",
        "██║╚██╗██║",
        "██║ ╚████║",
        "╚═╝  ╚═══╝"
    ],
    "O" : [
        " █████╗ ",
        "██╔══██╗",
        "██║  ██║",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "P" : [
        "██████╗ ",
        "██╔══██╗",
        "██████╔╝",
        "██╔═══╝ ",
        "██║     ",
        "╚═╝     "
    ],
    "Q" : [
        " █████╗  ",
        "██╔═══██╗",
        "██║   ██║",
        "██║▄▄ ██║",
        "╚██████╔╝",
        " ╚══▀▀═╝ "
    ],
    "R" : [
        "█████╗ ",
        "██╔═██╗",
        "█████╔╝",
        "██╔═██╗",
        "██║ ██║",
        "╚═╝ ╚═╝"
    ],
    "S" : [
        "██████╗",
        "██╔═══╝",
        "██████╗",
        "╚═══██║",
        "██████║",
        "╚═════╝"
    ],
    "T" : [
        "██████╗",
        "╚═██╔═╝",
        "  ██║  ",
        "  ██║  ",
        "  ██║  ",
        "  ╚═╝  "
    ],
    "U" : [
        "██╗  ██╗",
        "██║  ██║",
        "██║  ██║",
        "██║  ██║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "V" : [
        "██╗  ██╗",
        "██║  ██║",
        "██║  ██║",
        "╚██╗██╔╝",
        " ╚███╔╝ ",
        "  ╚══╝  "
    ],
    "W" : [
        "██╗    ██╗",
        "██║    ██║",
        "██║ █╗ ██║",
        "██║███╗██║",
        "╚███╔███╔╝",
        " ╚══╝╚══╝ "
    ],
    "X" : [
        "██╗  ██╗",
        "╚██╗██╔╝",
        " ╚███╔╝ ",
        " ██╔██╗ ",
        "██╔╝ ██╗",
        "╚═╝  ╚═╝"
    ],
    "Y" : [
        "██╗   ██╗",
        "╚██╗ ██╔╝",
        " ╚████╔╝ ",
        "  ╚██╔╝  ",
        "   ██║   ",
        "   ╚═╝   "
    ],
    "Z" : [
        "██████╗",
        "╚══██╔╝",
        "  ██╔╝ ",
        " ██╔╝  ",
        "██████╗",
        "╚═════╝"
    ],
    "0" : [
        " █████╗ ",
        "██╔═███╗",
        "██║██╔█║",
        "████╔╝█║",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "1" : [
        " ██╗",
        "███║",
        "╚██║",
        " ██║",
        " ██║",
        " ╚═╝"
    ],
    "2" : [
        "█████╗ ",
        "╚═══██╗",
        " ████╔╝",
        "██═══╝ ",
        "██████╗",
        "╚═════╝"
    ],
    "3" : [
        "█████╗ ",
        "╚═══██╗",
        " ████╔╝",
        " ╚══██╗",
        "█████╔╝",
        "╚════╝ "
    ],
    "4" : [
        "██╗ ██╗",
        "██║ ██║",
        "██████║",
        "╚═══██║",
        "    ██║",
        "    ╚═╝"
    ],
    "5" : [
        "██████╗",
        "██╔═══╝",
        "██████╗",
        "╚═══██║",
        "██████║",
        "╚═════╝"
    ],
    "6" : [
        " █████╗ ",
        "██╔═══╝ ",
        "██████╗ ",
        "██╔══██╗",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "7" : [
        "██████╗",
        "╚═══██║",
        "   ██╔╝",
        "  ██╔╝ ",
        "  ██║  ",
        "  ╚═╝  "
    ],
    "8" : [
        " █████╗ ",
        "██╔══██╗",
        "╚█████╔╝",
        "██╔══██╗",
        "╚█████╔╝",
        " ╚════╝ "
    ],
    "9" : [
        " █████╗ ",
        "██╔══██╗",
        "╚██████║",
        " ╚═══██║",
        " █████╔╝",
        " ╚════╝ "
    ],
    " " : [
        "  ",
        "  ",
        "  ",
        "  ",
        "  ",
        "  "
    ],
    "-" : [
        "      ",
        "      ",
        "█████╗",
        "╚════╝",
        "      ",
        "      "
    ],
    "/" : [
        "    █╗",
        "   █╔╝",
        "  █╔╝ ",
        " █╔╝  ",
        "█╔╝   ",
        "═╝    "
    ],
    "&" : [
        "    █╗",
        "   █╔╝",
        "  █╔╝ ",
        " █╔╝  ",
        "█╔╝   ",
        "═╝    "
    ],
    "_" : [
        "       ",
        "       ",
        "       ",
        "       ",
        "██████╗",
        "╚═════╝"
    ], 
    "." : [
        "   ",
        "   ",
        "   ",
        "   ",
        "██╗",
        "╚═╝"
    ]  
}

class FormatAsFiglet(sublime_plugin.TextCommand):
    # See https://github.com/patorjk/figlet-cli/blob/master/bin/figlet
    # Multiple lines must be multi-selected
    lines_to_insert = []

    @staticmethod
    def get_lines(title):
        upper = title.upper()
        print('Formatting2 as Figlet ANSI Shadow: ' + upper);
        i = 0
        upper_length = len(upper)
        lines = [
            "/*"
        ]
        while (i < 6):
            line = []
            j = 0;
            for letter in upper:
                try:
                    line.append(_figlet_letters[letter][i])
                except Exception:
                    pass
            lines.append("".join(line))
            i += 1
        lines.append("*/")
        return lines

    @staticmethod
    def format(title):
        return "\n".join(FormatAsFiglet.get_lines(title))

    def run(self, edit):
        # Decorate each region.
        view = self.view
        regions = len(view.sel())
        print("regions: ", regions)
        i = -1
        for region in view.sel():
            i += 1
            print("i: ", i)
            if not region.empty():
                print("region is not empty")
                # Pad inside selected region.
                title = view.substr(region)
                print("title: ", title)
                FormatAsFiglet.lines_to_insert.extend(FormatAsFiglet.get_lines(title))
                view.erase(edit, region)
                isInsertingSnippet = i == regions - 1
        for region in view.sel():
            view.sel().subtract(region)
        for region in view.sel():
            view.sel().subtract(region)
        if isInsertingSnippet:
            view.run_command("insert_snippet", { "contents": "\n".join(FormatAsFiglet.lines_to_insert)})

class AddDateCommand(sublime_plugin.TextCommand):
    @staticmethod
    def get_today():
        return "%s" %  datetime.date.today().strftime("%Y-%m-%d")

    def run(self, edit):
        self.view.run_command("insert_snippet", { "contents": AddDateCommand.get_today() } )

class AddTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", { "contents": "%s" %  datetime.datetime.now().strftime("%H:%M:%S %Z") } )

class FormatAsSectionTitleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        self.view.run_command("npm_run_arbitrary")

class AddCurrentVersionCommand(sublime_plugin.TextCommand):
    @staticmethod
    def get_header_region(view):
        return view.find("^\\/\\*\\*([\\s\\S]*?)\\*\\/", 0)

    @staticmethod
    def get_current_version_from_header(view, header_region):
        return re.findall("(@Version-[0-9\\.]+)", view.substr(header_region))[-1]

    @staticmethod
    def get_current_version(view):
        return AddCurrentVersionCommand.get_current_version_from_header(view, AddCurrentVersionCommand.get_header_region(view))

    @staticmethod
    def get_class_name(view):

        return view.substr(view.find(r" class (\w+)", 0, re.MULTILINE))[7:]

    @staticmethod
    def is_test(view):
        return not view.find(r"@IsTest", 0, re.MULTILINE).empty()

    def run(self, edit):
        header_region = self.view.find("^\\/\\*\\*([\\s\\S]*?)\\*\\/", 0)
        self.view.run_command("insert_snippet", { "contents": AddCurrentVersionCommand.get_current_version(self.view) })

class SaveListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if view.file_name() is not None and view.file_name().endswith((".js", ".page")):
            view.run_command("increment_console_version")

class IncrementConsoleVersionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = self.view.find_all("console\\.log\\('Version: \\d+'\\);")
        for region in regions:
            version = self.view.substr(region)
            self.view.replace(edit, region, re.sub(r"\d+", str(int(re.findall(r"\d+", version)[-1]) + 1), version))

class AddExceptionClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        offset = view.substr(view.line(view.sel()[0]))
        view.run_command("insert_snippet", { "contents": ("\n").join([
            "public virtual with sharing class ${1:Test}$2Exception extends $2Exception {",
                "\t/**",
                "\t *  ===${1/./=/g}============",
                "\t *     $1Exception",
                "\t *  ===${1/./=/g}============",
                "\t *  " + AddCurrentVersionCommand.get_current_version(view),
                "\t *  \t@Creatd",
                "\t *  \t@Added",
                "\t *  \t\t@" + AddCurrentVersionCommand.get_class_name(view),
                "\t *  \t\t\t@$1$2Exception",
                "\t *  \t\t\t\t@Extends",
                "\t *  \t\t\t\t\t@$2Exception",
                "\t*/",
                "}",
                ""
        ])})

class AddInnerClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        offset = view.substr(view.line(view.sel()[0]))
        view.run_command("insert_snippet", { "contents": ("\n").join([
            "public with sharing class ${1:InnerClass} {",
                "\t/**",
                "\t *  ===${1/./=/g}===",
                "\t *     $1",
                "\t *  ===${1/./=/g}===",
                "\t *  " + AddCurrentVersionCommand.get_current_version(view),
                "\t *  \t@Created",
                "\t *  \t@Description",
                "\t *  \t@Added",
                "\t *  \t\t@" + AddCurrentVersionCommand.get_class_name(view),
                "\t *  \t\t\t@$1",
                "\t *  \t\t\t\t@Variables",
                "\t *  \t\t\t\t\t@Private",
                "\t *  \t\t\t\t\t\t",
                "\t *  \t\t\t\t@Constructors",
                "\t *  \t\t\t\t\t@Public",
                "\t *  \t\t\t\t\t\t$1()",
                "\t *  \t\t\t\t@Methods",
                "\t *  \t\t\t\t\t@Public",
                "\t *  \t\t\t\t\t\t",
                "\t*/",
            "}",
            ""
        ])})

class AddInnerClassCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        offset = view.substr(view.line(view.sel()[0]))
        view.run_command("insert_snippet", { "contents": ("\n").join([
            "/**",
            " *  ===${1/./=/g}===",
            " *     $1",
            " *  ===${1/./=/g}===",
            " *  " + AddCurrentVersionCommand.get_current_version(view),
            " *  \t@Created",
            " *  \t@Description",
            " *  \t@Added",
            " *  \t\t@" + AddCurrentVersionCommand.get_class_name(view),
            " *  \t\t\t@$1",
            " *  \t\t\t\t@Variables",
            " *  \t\t\t\t\t@Private",
            " *  \t\t\t\t\t\t",
            " *  \t\t\t\t@Constructors",
            " *  \t\t\t\t\t@Public",
            " *  \t\t\t\t\t\t$1()",
            " *  \t\t\t\t@Methods",
            " *  \t\t\t\t\t@Public",
            " *  \t\t\t\t\t\t",
            "*/",
        ])})

class AddMethodCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        line_region = view.line(view.sel()[0])
        line = view.substr(line_region)
        header_region = AddCurrentVersionCommand.get_header_region(view)
        is_header = header_region.contains(line_region)
        
        class_name = AddCurrentVersionCommand.get_class_name(view)
        border = "=" * (len(class_name) + 6)
        is_test = AddCurrentVersionCommand.is_test(view)

        if re.match(".*\\*.*", line):
            # inside a comment
            line_delimiter = "\n" + re.findall(r"^(.*)(?=\*)", line)[-1] + "*  "
            version = AddCurrentVersionCommand.get_current_version_from_header(view, header_region)
            footer = "\t"

            # in the header
            if is_header:
                version = re.sub(r"\d+$", str(int(re.findall(r"\d+$", version)[-1]) + 1), version)
                footer = line_delimiter.join([
                    "\t@Date",
                    "\t\t" + AddDateCommand.get_today(),
                    "\t@Author",
                    "\t\t" + view.settings().get('tm_fullname'),
                    "\t@Created",
                    "\t@Description",
                    "\t@Added", 
                    "\t\t@" + class_name,
                    "\t\t\t@Variables",
                    "\t\t\t\t@Private",
                    "\t\t\t\t\t",
                    "\t\t\t@Constructors",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t",
                    "\t\t\t@Methods",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t",
                    "\t\t\t@Static",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t@InnerClass",
                    "\t\t\t\t@Constructors",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t@Changed",
                    "\t\t@" + class_name,
                    "\t\t\t@Constructors",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t",
                    "\t\t\t@Methods",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t",
                    "\t\t\t@Static",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t@InnerClass",
                    "\t\t\t\t@Constructors",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                ])
            view.replace(edit, line_region, line_delimiter.join([
                re.sub("\\*.*", "" , line) + "*  " + version,
                footer
            ]))
        else:
            # not inside a comment
            line_delimiter = "\n *  "
            if view.sel()[0].begin() == 0: 
                # in the header
                if(is_test):
                    tests = ""
                else:
                    tests = line_delimiter.join([
                        "",
                        "@UnitTests",
                        "\t" + class_name + "_test"
                    ])

                view.run_command("insert_snippet", { "contents": line_delimiter.join([
                    "/**",
                    border,
                    "   " + class_name + "   ",
                    border + tests,
                    "@Version-1.0.0",
                    "\t@Date", 
                    "\t\t" + AddDateCommand.get_today(), 
                    "\t@Author", 
                    "\t\t" + view.settings().get('tm_fullname'), 
                    "\t@Created",
                    "\t@Description",
                    "\t@Added",  
                    "\t\t@" + class_name, 
                    "\t\t\t@Variables",
                    "\t\t\t\t@Private",
                    "\t\t\t\t\t",
                    "\t\t\t@Constructors",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t",
                    "\t\t\t@Methods",
                    "\t\t\t\t@Public",
                    "\t\t\t\t\t\t\t",
                    "\t\t\t@Static",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t@InnerClass",
                    "\t\t\t\t@Constructors",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                    "\t\t\t\t@Methods",
                    "\t\t\t\t\t@Public",
                    "\t\t\t\t\t\t",
                ]) + "\n*/"})
            else:
                # not in the header
                lines = [
                    "/**"
                ]

                lines.extend([
                    AddCurrentVersionCommand.get_current_version(view),
                    "\t@Created",
                    "\t@Throws",
                    "\t\t@Exception",
                    "\t\t\t@When",
                    "\t\t\t\t",
                    "\t@Sets",
                    "\t\t", 
                    "\t@Returns",
                    "\t\t$1"
                ])
                view.run_command("insert_snippet", { "contents": line_delimiter.join(lines) + "\n*/"})

class AddVariableCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", { "contents": "// "})
        self.view.run_command("add_current_version")

class AddDescriptionCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_snippet", { "contents": "@Description\n*  \t"})

class AddTestMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        offset= len(WrapSelectionAsTitleCommand.replace_tabs_with_spaces(view, view.substr(view.full_line(view.sel()[0]))))
        class_name = AddCurrentVersionCommand.get_class_name(view)
        if class_name.endswith('_Test'):
            class_name = class_name[:-5]

        view.run_command("insert_snippet", { 
            "contents": "\n".join([
                "@IsTest",
                "public static void test${1:Utilites}() {",
                "\t" + "\n\t".join([
                    "/**",
                    " *  " + AddCurrentVersionCommand.get_current_version(view),
                    " *  \t@Created",
                    " *  \t@Description",
                    " *  \t@Added",
                    " *  \t\t@" + class_name,
                    " *  \t\t\t@$1",
                    " *  \t\t\t\t@Constructors",
                    " *  \t\t\t\t\t",
                    " *  \t\t\t\t@Methods",
                    " *  \t\t\t\t\t",
                    "*/",
                    "// Data",
                    "",
                    WrapSelectionAsTitleCommand.get_title("Start Test", offset),
                    "Test.startTest();"
                    "",
                    "",
                    "",
                    "Test.stopTest();",
                    WrapSelectionAsTitleCommand.get_title("Stop Test", offset)
                ]),
                "}"
            ])
        })        

class WrapSelectionAsTitleCommand(sublime_plugin.TextCommand):
    # See https://github.com/mborgerson/Pad/blob/master/pad.py
    # Multiple lines must be multi-selected

    @staticmethod
    def get_title(title, offset):
        fill_width = 110 - offset
        if title:
            fill_width = (fill_width - len(title) - 7) // 2
        else:
            title = ""
        fill_char = "-"
        return "// " + (fill_char * fill_width) + "  " + title + "  " + (fill_char * fill_width)

    @staticmethod
    def replace_tabs_with_spaces(view, text):
        if text:
            return re.sub(r"\t", " " * view.settings().get("tab_size"), text, 0, re.MULTILINE)
        else:
            return ""

    def run(self, edit, fill_char="-", width=110, align_char=">"):
        # Decorate each region.
        view = self.view
        for region in view.sel():
            line = view.line(region)
            if region.empty():
                # No text selected, pad entire line title.
                title = view.substr(line)
                offset = 0
                replace_region = line
            else:
                # Pad inside selected region.
                title = view.substr(region)
                offset = len(WrapSelectionAsTitleCommand.replace_tabs_with_spaces(view, view.substr(line)[:-len(title)]))
                replace_region = region
            view.replace(edit, replace_region, WrapSelectionAsTitleCommand.get_title(title, offset))