import pytest
from src.creation.get_tools import get_tools_from_agent
from src.models import AgentTools, ToolInfo
from example_agent.agent import root_agent


def test_get_tools_from_agent_with_real_agent():
    """Test get_tools_from_agent with the actual root_agent from example_agent."""
    result = get_tools_from_agent(root_agent)

    # Verify the result is an AgentTools instance
    assert isinstance(result, AgentTools)
    assert result.agent_name == "time_agent"

    # Verify tools are extracted
    assert len(result.tools) > 0

    # Check that each tool has the expected structure
    for tool in result.tools:
        assert isinstance(tool, ToolInfo)
        assert tool.name is not None
        assert tool.description is not None


def test_get_tools_from_agent_with_mock_agent(mocker):
    """Test get_tools_from_agent with a mock agent that has tools."""
    # Create a mock tool
    mock_tool = mocker.Mock()
    mock_tool.name = "test_tool"
    mock_tool.description = "A test tool for testing purposes"
    mock_tool.parameters = {"param1": "string"}

    # Create a mock agent
    mock_agent = mocker.Mock()
    mock_agent.name = "test_agent"
    mock_agent.tools = [mock_tool]

    result = get_tools_from_agent(mock_agent)

    # Verify the result
    assert isinstance(result, AgentTools)
    assert result.agent_name == "test_agent"
    assert len(result.tools) == 1

    tool = result.tools[0]
    assert tool.name == "test_tool"
    assert tool.description == "A test tool for testing purposes"
    assert tool.parameters == {"param1": "string"}


def test_get_tools_from_agent_with_no_tools(mocker):
    """Test get_tools_from_agent with an agent that has no tools."""
    mock_agent = mocker.Mock()
    mock_agent.name = "empty_agent"
    mock_agent.tools = []

    result = get_tools_from_agent(mock_agent)

    assert isinstance(result, AgentTools)
    assert result.agent_name == "empty_agent"
    assert len(result.tools) == 0


def test_get_tools_from_agent_with_tool_no_attributes(mocker):
    """Test get_tools_from_agent with a tool that doesn't have name/description attributes."""
    # Create a tool without name/description attributes
    mock_tool = mocker.Mock()
    # Don't set name or description attributes

    mock_agent = mocker.Mock()
    mock_agent.name = "test_agent"
    mock_agent.tools = [mock_tool]

    result = get_tools_from_agent(mock_agent)

    assert isinstance(result, AgentTools)
    assert len(result.tools) == 1

    tool = result.tools[0]
    # Should fall back to string representation for name
    assert tool.name == str(mock_tool)
    # Should have default description
    assert tool.description == "No description available"


def test_get_tools_from_agent_without_name(mocker):
    """Test get_tools_from_agent with an agent that doesn't have a name attribute."""
    mock_agent = mocker.Mock()
    mock_agent.tools = []
    # Don't set name attribute

    result = get_tools_from_agent(mock_agent)

    assert isinstance(result, AgentTools)
    assert result.agent_name == "Unknown Agent"


def test_get_tools_from_agent_without_tools_attribute(mocker):
    """Test get_tools_from_agent with an agent that doesn't have a tools attribute."""
    mock_agent = mocker.Mock()
    mock_agent.name = "test_agent"
    # Don't set tools attribute

    result = get_tools_from_agent(mock_agent)

    assert isinstance(result, AgentTools)
    assert result.agent_name == "test_agent"
    assert len(result.tools) == 0


def test_tool_info_structure():
    """Test that ToolInfo instances have the correct structure."""
    tool_info = ToolInfo(
        name="test_tool",
        description="Test description",
        parameters={"test_param": "string"},
    )

    assert tool_info.name == "test_tool"
    assert tool_info.description == "Test description"
    assert tool_info.parameters == {"test_param": "string"}


def test_agent_tools_structure():
    """Test that AgentTools instances have the correct structure."""
    tool_info = ToolInfo(
        name="test_tool", description="Test description", parameters=None
    )

    agent_tools = AgentTools(tools=[tool_info], agent_name="test_agent")

    assert agent_tools.agent_name == "test_agent"
    assert len(agent_tools.tools) == 1
    assert agent_tools.tools[0].name == "test_tool"
