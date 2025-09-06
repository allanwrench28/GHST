# Copilot Instructions for GHST

## Overview
GHST is an open-source AI coding engine designed to facilitate collaboration among expert AI agents for coding, debugging, and creative problem-solving. This document provides essential guidance for AI agents to be productive in this codebase.

## Architecture
- **AI Collaboration Framework**: Multiple AI agents work together to analyze, generate, and improve code. Understanding the interactions between these agents is crucial for effective collaboration.
- **Plugin System**: The architecture supports modular plugins, allowing for easy extension of features. Key files include `src/plugins/` for plugin development and `src/ui_components/` for UI integration.
- **Configuration Management**: Settings are managed through a YAML-based system located in the `config/` directory. Familiarity with these configurations is essential for customizing the environment.

## Developer Workflows
- **Building**: Use the provided scripts in the `scripts/` directory for building and testing the application. The `nightly_build.py` script automates the build process.
- **Testing**: Tests are located in the `test_*.py` files. Run tests using the command `pytest` from the root directory to ensure code quality.
- **Debugging**: Utilize the built-in logging features in `src/utils/config_manager.py` to trace issues effectively.

## Project-Specific Conventions
- **Code Structure**: Follow the established directory structure for organizing code. For example, all AI-related functionalities should reside in `src/ai_collaboration/`.
- **Naming Conventions**: Use descriptive names for functions and classes to enhance readability. For instance, `ghost_manager.py` manages ghost-related functionalities.

## Integration Points
- **External Dependencies**: Manage dependencies through `requirements.txt`. Ensure all necessary packages are installed using `pip install -r requirements.txt`.
- **Cross-Component Communication**: Components communicate through well-defined interfaces. Review the `src/plugins/plugin_manager.py` for examples of how plugins interact with the core system.

## Key Files and Directories
- **Main Application**: `launch_gui.py` serves as the entry point for the application.
- **Documentation**: Refer to `docs/` for comprehensive guides and rulesets.
- **Examples**: Check `examples/` for practical implementations of various features.

## GHSTs as PHD Themes

GHSTs (Ghosts) serve as the central themes for PhD research within the GHST framework. Each GHST represents a unique area of exploration and innovation, guiding research efforts and collaboration among AI agents. The following themes are identified:

1. **AI Collaboration**: Exploring the dynamics of multiple AI agents working together to solve complex problems.
2. **Ethical AI**: Investigating the ethical implications and frameworks for AI development and deployment.
3. **Plugin Development**: Focusing on the creation and integration of modular plugins to enhance functionality.
4. **User Interface Design**: Studying the design principles for creating intuitive and effective user interfaces for AI applications.
5. **Data Management**: Addressing challenges in data handling, storage, and processing within AI systems.

These themes not only guide research but also foster a collaborative environment for innovation and knowledge sharing.

## Multiple Different Personalities

In the context of GHST, multiple different personalities refer to the various AI agents that can collaborate and interact within the framework. Each personality can be designed to specialize in different areas, such as problem-solving, ethical considerations, or user interaction. This diversity allows for a more robust and adaptable system, enhancing the overall effectiveness of the AI collaboration.

### Key Aspects of Different Personalities:
1. **Specialization**: Each personality can focus on specific tasks or domains, improving efficiency and expertise.
2. **Collaboration**: Personalities can work together, leveraging their unique strengths to tackle complex challenges.
3. **Adaptability**: The system can adjust to different scenarios by activating the most suitable personalities for the task at hand.

This approach not only enriches the user experience but also fosters innovation through diverse perspectives and methodologies.

## Personality Engines for PhD GHSTs

The Personality Engines for PhD GHSTs are designed to enhance user interaction by randomizing names and offering slightly varying fields of study. This approach ensures that each interaction remains valuable and tailored to the user's input. 

### Core Features:
1. **Randomized Names**: Each GHST can have a unique name generated from a predefined list, adding a layer of personalization.
2. **Varying Fields of Study**: While maintaining a core set of expertise, GHSTs can present slightly different perspectives or specialties, enriching the user's experience.
3. **Think Tanks**: A core set of GHSTs can function as think tanks, collaborating on complex problems and providing diverse insights.
4. **Recruitment from the Engine**: Users can recruit additional GHSTs from the engine, allowing for a dynamic and evolving interaction based on their needs.

This system not only fosters creativity and innovation but also ensures that users receive a comprehensive and engaging experience tailored to their specific inquiries.

## Conclusion
This document serves as a foundational guide for AI agents working within the GHST codebase. For further details, refer to the specific files mentioned above and the overall project documentation.
