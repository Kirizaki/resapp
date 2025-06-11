# app/runner.py
from app.scrapers.scraper_factory import ScraperFactory
from app.utils.logger import Logger
from app.db.database_processor import DatabaseProcessor
from app.scrapers.scraper_runner import ScraperRunner

import asyncio
import argparse
import json

logger = Logger().get_logger()


def parse_args():
    parser = argparse.ArgumentParser(description="RESapp (Real Estate Scraper Application)")
    parser.add_argument("--site", required=True, help="Name of the site to scrape (e.g. otodom)")
    parser.add_argument("--config", help="Path to JSON file with config (optional)")
    return parser.parse_args()


def load_config(path: str) -> dict:
    try:
        with open(path, "r") as f:
            config = json.load(f)
            logger.debug("Loaded config from file", extra={"config": config})
            return config
    except Exception as _:
        logger.error("Failed to load config", exc_info=True)
        return {}


def run_scrapers(site: str, config: dict) -> None:
    scraper = ScraperFactory.create(site, config)  ## create N scrapers from config based on config data itself
    logger.info("Starting scrapers", extra={"site": site})
    processor = DatabaseProcessor()
    runner = ScraperRunner([scraper], processor)

    asyncio.run(runner.run())
    logger.info("Scrapers finished", extra={"site": site, "count": len(results)})


if __name__ == "__main__":
    # try:
    args = parse_args()
    config = load_config(args.config) if args.config else {}
    run_scrapers(args.site, config)
    # except Exception as e:
    #     print(e)
        # logger.error(e)
