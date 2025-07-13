import pytest
from src.runner.scenario_runner import call_agent_async, run_scenario
from src.models import Scenario
from example_agent.agent import root_agent


@pytest.mark.asyncio
async def test_scenario_runner():
    events = await call_agent_async(
        agent=root_agent,
        query="Flip a coin",
        user_id="test_user",
        session_id="test_session",
        app_name="test_app",
    )

    assert len(events) > 0
    assert events is not None


class TestRunScenario:
    """Test cases for the run_scenario function."""

    @pytest.fixture
    def mock_agent(self, mocker):
        """Create a mock agent for testing."""
        agent = mocker.MagicMock()
        agent.name = "test_agent"
        return agent

    @pytest.fixture
    def scenario_no_tool_expected(self):
        """Create a scenario with no expected tool call."""
        return Scenario(
            name="no_tool_scenario",
            query="Just answer a question",
            why_its_suitable="Tests basic conversation",
            expected_tool_call=None,
        )

    @pytest.fixture
    def scenario_with_tool_expected(self):
        """Create a scenario with expected tool call."""
        return Scenario(
            name="tool_scenario",
            query="What time is it?",
            why_its_suitable="Tests tool usage",
            expected_tool_call="get_current_time",
        )

    def create_mock_event(self, mocker, function_calls=None):
        """Create a mock event with optional function calls."""
        event = mocker.MagicMock()
        event.get_function_calls.return_value = function_calls or []
        return event

    @pytest.mark.asyncio
    async def test_run_scenario_no_tool_expected_no_calls_made(
        self, mocker, mock_agent, scenario_no_tool_expected
    ):
        """Test scenario where no tool is expected and no function calls are made."""
        # Mock call_agent_async to return events with no function calls
        mock_events = [self.create_mock_event(mocker)]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_no_tool_expected, mock_agent)

        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_no_tool_expected_but_calls_made(
        self, mocker, mock_agent, scenario_no_tool_expected
    ):
        """Test scenario where no tool is expected but function calls are made."""
        # Mock call_agent_async to return events with function calls
        mock_events = [self.create_mock_event(mocker, ["unexpected_function_call"])]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_no_tool_expected, mock_agent)

        assert result is False

    @pytest.mark.asyncio
    async def test_run_scenario_tool_expected_and_called(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test scenario where expected tool call is made."""
        # Mock call_agent_async to return events with the expected function call
        mock_events = [self.create_mock_event(mocker, ["get_current_time"])]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_with_tool_expected, mock_agent)

        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_tool_expected_but_not_called(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test scenario where expected tool call is not made."""
        # Mock call_agent_async to return events with no function calls
        mock_events = [self.create_mock_event(mocker)]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_with_tool_expected, mock_agent)

        assert result is False

    @pytest.mark.asyncio
    async def test_run_scenario_tool_expected_different_tool_called(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test scenario where different tool is called than expected."""
        # Mock call_agent_async to return events with different function call
        mock_events = [self.create_mock_event(mocker, ["different_function_call"])]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_with_tool_expected, mock_agent)

        assert result is False

    @pytest.mark.asyncio
    async def test_run_scenario_multiple_events_with_function_calls(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test scenario with multiple events containing function calls."""
        # Mock call_agent_async to return multiple events with function calls
        mock_events = [
            self.create_mock_event(mocker, ["other_function"]),
            self.create_mock_event(mocker, ["get_current_time"]),
            self.create_mock_event(mocker, ["another_function"]),
        ]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_with_tool_expected, mock_agent)

        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_multiple_events_no_expected_call(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test scenario with multiple events but no expected function call."""
        # Mock call_agent_async to return multiple events without expected call
        mock_events = [
            self.create_mock_event(mocker, ["other_function"]),
            self.create_mock_event(mocker, ["another_function"]),
            self.create_mock_event(mocker, ["third_function"]),
        ]

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_with_tool_expected, mock_agent)

        assert result is False

    @pytest.mark.asyncio
    async def test_run_scenario_empty_events(
        self, mocker, mock_agent, scenario_no_tool_expected
    ):
        """Test scenario with empty events list."""
        # Mock call_agent_async to return empty events
        mock_events = []

        mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        result = await run_scenario(scenario_no_tool_expected, mock_agent)

        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_call_agent_async_parameters(
        self, mocker, mock_agent, scenario_with_tool_expected
    ):
        """Test that run_scenario passes correct parameters to call_agent_async."""
        mock_events = [self.create_mock_event(mocker, ["get_current_time"])]

        mock_call = mocker.patch(
            "src.runner.scenario_runner.call_agent_async", return_value=mock_events
        )
        await run_scenario(scenario_with_tool_expected, mock_agent)

        # Verify call_agent_async was called with correct parameters
        mock_call.assert_called_once_with(
            mock_agent,
            scenario_with_tool_expected.query,
            ("1",),  # user_id
            ("2",),  # session_id
            ("3",),  # app_name
        )


class TestRunScenarioIntegration:
    """Integration tests for run_scenario function with real ADK agent."""

    @pytest.fixture
    def time_scenario_with_tool_expected(self):
        """Create a scenario that should trigger time tool usage."""
        return Scenario(
            name="time_query_scenario",
            query="What time is it right now?",
            why_its_suitable="Tests time tool integration",
            expected_tool_call="get_current_time",
        )

    @pytest.fixture
    def time_scenario_different_phrasing(self):
        """Create a scenario with different phrasing that should trigger time tool."""
        return Scenario(
            name="time_query_alt_scenario",
            query="Can you tell me the current time?",
            why_its_suitable="Tests time tool with different phrasing",
            expected_tool_call="get_current_time",
        )

    @pytest.fixture
    def conversation_scenario_no_tool(self):
        """Create a scenario that should not trigger any tools."""
        return Scenario(
            name="conversation_scenario",
            query="Hello, how are you doing today?",
            why_its_suitable="Tests basic conversation without tools",
            expected_tool_call=None,
        )

    @pytest.fixture
    def math_scenario_no_tool(self):
        """Create a scenario that should not trigger tools (agent doesn't have math tools)."""
        return Scenario(
            name="math_scenario",
            query="What is 2 + 2?",
            why_its_suitable="Tests math query without specialized tools",
            expected_tool_call=None,
        )

    @pytest.mark.asyncio
    async def test_run_scenario_time_query_success(
        self, time_scenario_with_tool_expected
    ):
        """Test that time query scenario successfully calls time tool."""
        result = await run_scenario(time_scenario_with_tool_expected, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_time_query_alt_phrasing(
        self, time_scenario_different_phrasing
    ):
        """Test that differently phrased time query also works."""
        result = await run_scenario(time_scenario_different_phrasing, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_conversation_no_tool(
        self, conversation_scenario_no_tool
    ):
        """Test that conversation scenario doesn't trigger tools."""
        result = await run_scenario(conversation_scenario_no_tool, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_math_no_tool(self, math_scenario_no_tool):
        """Test that math scenario doesn't trigger tools (agent has no math tools)."""
        result = await run_scenario(math_scenario_no_tool, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_timezone_query(self):
        """Test more complex time-related query."""
        scenario = Scenario(
            name="timezone_scenario",
            query="What timezone am I in and what time is it?",
            why_its_suitable="Tests complex time query",
            expected_tool_call="get_current_time",
        )
        result = await run_scenario(scenario, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_weather_query_no_tool(self):
        """Test scenario that should not trigger tools (agent doesn't have weather tools)."""
        scenario = Scenario(
            name="weather_scenario",
            query="What's the weather like today?",
            why_its_suitable="Tests query for non-available tool",
            expected_tool_call=None,
        )
        result = await run_scenario(scenario, root_agent)
        assert result is True

    @pytest.mark.asyncio
    async def test_run_scenario_multiple_time_queries(self):
        """Test multiple time-related scenarios to ensure consistency."""
        time_scenarios = [
            Scenario(
                name="time_now",
                query="What time is it now?",
                why_its_suitable="Direct time query",
                expected_tool_call="get_current_time",
            ),
            Scenario(
                name="current_time",
                query="Can you show me the current time?",
                why_its_suitable="Current time request",
                expected_tool_call="get_current_time",
            ),
            Scenario(
                name="time_check",
                query="I need to check the time",
                why_its_suitable="Time checking request",
                expected_tool_call="get_current_time",
            ),
        ]

        for scenario in time_scenarios:
            result = await run_scenario(scenario, root_agent)
            assert result is True, f"Failed for scenario: {scenario.name}"
