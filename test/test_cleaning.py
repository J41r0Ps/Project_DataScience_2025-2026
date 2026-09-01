import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.cleaning import (
    clean_missing,
    parse_distance,
    parse_time_hours,
    parse_points,
    parse_rider_name,
)


class TestCleanMissing:
    """Wikipedia encodes 'no data' as an em-dash, not an empty cell."""

    @pytest.mark.parametrize("value", ["—", "–", "-", "", "   "])
    def test_placeholders_become_nan(self, value):
        assert clean_missing(value) is np.nan

    def test_none_becomes_nan(self):
        assert clean_missing(None) is np.nan

    def test_real_value_survives(self):
        assert clean_missing("Maurice Garin") == "Maurice Garin"


class TestParseDistance:
    def test_strips_thousands_separator_and_miles(self):
        assert parse_distance("2,428km (1,509mi)") == 2428.0

    def test_handles_four_digit_distance(self):
        assert parse_distance("5,745km (3,570mi)") == 5745.0

    def test_missing_returns_nan(self):
        assert np.isnan(parse_distance("—"))

    def test_anchors_on_km_not_first_number(self):
        """The km figure must be taken, never the miles conversion."""
        assert parse_distance("3,245km (2,016mi)") == 3245.0


class TestParseTimeHours:
    def test_parses_typographic_primes(self):
        """Wikipedia uses ′ (U+2032) and ″ (U+2033), not ASCII quotes."""
        result = parse_time_hours("94h 33′ 14″")
        assert result == pytest.approx(94.5539, abs=1e-4)

    def test_seconds_are_optional(self):
        assert parse_time_hours("94h 33′") == pytest.approx(94.55, abs=1e-2)

    def test_points_value_returns_nan(self):
        """A bare integer is a point total, not a duration."""
        assert np.isnan(parse_time_hours("35"))

    def test_missing_returns_nan(self):
        assert np.isnan(parse_time_hours("—"))


class TestParsePoints:
    def test_bare_integer_is_points(self):
        assert parse_points("35") == 35.0

    def test_duration_returns_nan(self):
        assert np.isnan(parse_points("94h 33′ 14″"))

    def test_missing_returns_nan(self):
        assert np.isnan(parse_points("—"))


class TestParseRiderName:
    def test_plain_name_unchanged(self):
        result = parse_rider_name("Maurice Garin")
        assert result["rider_name"] == "Maurice Garin"
        assert result["is_reassigned"] is False
        assert result["no_winner"] is False

    def test_footnote_marker_stripped(self):
        assert parse_rider_name("Henri Cornet[b]")["rider_name"] == "Henri Cornet"

    def test_accents_preserved(self):
        assert parse_rider_name("Óscar Pereiro[d]")["rider_name"] == "Óscar Pereiro"

    @pytest.mark.parametrize("raw,expected", [
        ("Andy Schleck#[e]", "Andy Schleck"),
        ("Michele Scarponi†[a]", "Michele Scarponi"),
    ])
    def test_reassigned_titles_flagged(self, raw, expected):
        """'#' and '†' mark titles awarded after the original winner was stripped."""
        result = parse_rider_name(raw)
        assert result["rider_name"] == expected
        assert result["is_reassigned"] is True

    def test_no_winner_flagged_separately(self):
        """TdF 1999-2005: the race happened, the result was annulled."""
        result = parse_rider_name("No winner[a]")
        assert np.isnan(result["rider_name"])
        assert result["no_winner"] is True

    def test_war_year_is_not_a_disputed_result(self):
        """An em-dash means no race was held - different from an annulled result."""
        result = parse_rider_name("—")
        assert np.isnan(result["rider_name"])
        assert result["no_winner"] is False