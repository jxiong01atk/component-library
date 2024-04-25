from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DECIMAL, DateTime, CHAR, Boolean, func, Float, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import pyodbc

dbstring = 'mssql+pyodbc://client:root@20.159.218.61,1433/L3Harris?driver=SQL+Server'

Base = declarative_base()

class Spendcube(Base):
    __tablename__ = 'SPENDCUBE'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer = Column(String)
    actual_pay_date = Column(DateTime, nullable=True)
    invoice_number = Column(String)
    po_number = Column(String)
    po_line = Column(String)
    segment = Column(String)
    sector = Column(String)
    division = Column(String)
    site_location = Column(String)
    unit = Column(String)
    subunit = Column(String)
    program_area = Column(String)
    business_area = Column(String)
    project = Column(String)
    company_code = Column(String)
    data_source = Column(String)
    supplier_name = Column(String)
    erp_supplier_id = Column(String)
    std_supplier_id = Column(String)
    mdg_id = Column(String)
    physical_city = Column(String)
    physical_state = Column(String)
    physical_country = Column(String)
    physical_address = Column(String)
    naics = Column(String)
    category_team = Column(String)
    supplier_level_1 = Column(String)
    supplier_level_2 = Column(String)
    supplier_level_3 = Column(String)
    pt_group_value = Column(String)
    pay_terms = Column(String)
    order_date_inv = Column(DateTime)
    invoice_date = Column(DateTime)
    invoice_description = Column(String)
    part = Column(String)
    part_description = Column(String)
    mfr_part = Column(String)
    commodity_desc_po = Column(String)
    commodity_code_po = Column(String)
    quantity = Column(Float)
    spend = Column(Float)
    mpn = Column(String)
    price = Column(Float)
    # in_scope_part_id = Column(String)
    # part_rationale = Column(String)
    # data_quality = Column(String)
    segment_reclassify = Column(String)
    sector_reclassify = Column(String)
    category_team_remapping = Column(String)
    # forecast_description = Column(String)
    supplier_name_standardized = Column(String)
    supplier_in_wave_1 = Column(String)

class Forecasts(Base):
    __tablename__ = 'FORECASTS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_source = Column(String)
    UID = Column(String)
    segment = Column(String)
    sector = Column(String)
    division = Column(String)
    business_unit = Column(String)
    site = Column(String)
    lh_x_part_number = Column(String)
    mpn = Column(String)
    mpn_trim = Column(String)
    mpn_modifier = Column(String)
    pn_description = Column(String)
    std_mfg_final = Column(String)
    est_annual_usage = Column(DECIMAL(10, 2))
    historical_base_unit_price = Column(DECIMAL(10, 2))
    ext_spend = Column(DECIMAL(10, 2))
    ext_spend_m = Column(DECIMAL(10, 2))
    incumbent_distributor_name = Column(String)
    contract_manufacturer = Column(String)
    program_name_product_line = Column(String)
    site_commodity = Column(String)
    supplemental_oem_lookup = Column(String)
    supplier_standardized = Column(String)
    mpn_2023 = Column(String)
    lh_x_part_2023 = Column(String)
    mpn_trim_2023 = Column(String)
    mpn_2022 = Column(String)
    lh_x_part_2022 = Column(String)
    mpn_trim_2022 = Column(String)
    historical_price = Column(DECIMAL(10, 2))
    base_forecast = Column(DECIMAL(10, 2))
    mpn_2023f = Column(String)
    lh_x_part_2023f = Column(String)
    mpn_trim_2023f = Column(String)
    forecast_2023f = Column(String)
    price_data_request = Column(DECIMAL(10, 2))
    final_price_tcom = Column(DECIMAL(10, 2))
    final_price_non_tcom = Column(DECIMAL(10, 2))
    price_final = Column(DECIMAL(10, 2))
    price_source = Column(DECIMAL(10, 2))
    ma_supplemental = Column(DECIMAL(10, 2))
    qty_data_request = Column(DECIMAL(10, 2))
    qty_2024f = Column(DECIMAL(10, 2))
    qty_savanna = Column(DECIMAL(10, 2))
    qty_final = Column(DECIMAL(10, 2))
    price_matched = Column(DECIMAL(10, 2))
    data_from_other_sources = Column(DECIMAL(10, 2))
    forecast_2024_kearney = Column(DECIMAL(10, 2))
    on_f_35_agreement = Column(String)
    pricing_agreement_in_place = Column(String)
    supplier_in_scope = Column(String)
    recognizable_supplier = Column(String)
    site_standardized = Column(String)
    sector_standardized = Column(String)
    site_sector = Column(String)
    sector_lh_x_part = Column(String)
    sector_mpn = Column(String)
    lh_x_part_site = Column(String)
    mpn_site = Column(String)
    sprint = Column(String)
    lh_x_mpn_mpn_trim = Column(String)
    site_sector_combined = Column(String)
    commodity_mpn = Column(String)
    commodity_mpn_trim = Column(String)
    commodity_final = Column(String)
    manufacturer_provided_2024f = Column(String)
    manufacturer_silicon_experts = Column(String)
    manufacturer_bid_sheet = Column(String)
    matches = Column(String)
    include_in_sprint_4 = Column(String)
    include_manufacturer = Column(String)
    addressable_spend = Column(DECIMAL(10, 2))
    price_all = Column(DECIMAL(10, 2))
    price_2024f = Column(DECIMAL(10, 2))
    price_2023f = Column(DECIMAL(10, 2))
    price_historical = Column(DECIMAL(10, 2))
    manufacturer_standardized = Column(String)
    sprint_standardized_manufacturer = Column(String)


class Idea(Base):
    __tablename__ = 'IDEAS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String)
    type = Column(String)
    description = Column(String)
    status = Column(String)
    il = Column(String)
    notes = Column(String)
    alternate_pn = Column(String)
    baseline_cost_source = Column(Integer, ForeignKey('PART_COSTS.id'))
    custom_baseline_cost = Column(DECIMAL(10, 2), default=0.00) 
    target_cost = Column(DECIMAL(10, 2), default=0.00)
    confirmed_cost = Column(DECIMAL(10, 2), default=0.00)
    toggle_active = Column(Boolean, default=True, nullable=False)  
    datetime_added = Column(DateTime, default=func.current_timestamp())  
    
    # Relationships
    parts = relationship('Part', secondary = "PART_HAS_IDEA", back_populates='ideas')
    volumes = relationship("PartCosts",secondary="IDEA_HAS_VOLUMES", back_populates="ideas_at_volume")


class Part(Base):
    __tablename__ = 'PARTS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_number = Column(String)
    description = Column(String)
    datetime_added = Column(DateTime, default=func.current_timestamp()) 
    
    ideas = relationship("Idea", secondary='PART_HAS_IDEA', back_populates="parts")
    products = relationship("Product", secondary='PART_IN_PRODUCT', back_populates = "parts")
    prices = relationship("PartCosts", back_populates="part", cascade='all, delete, delete-orphan')
    mpns = relationship("MPNS", secondary="PARTS_MPNS", back_populates="parts")

class PartHasIdea(Base):
    __tablename__ = 'PART_HAS_IDEA'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('PARTS.id', ondelete='CASCADE'))
    idea_id = Column(Integer, ForeignKey('IDEAS.id', ondelete='CASCADE'))
    datetime_added = Column(DateTime, default=func.current_timestamp()) 


class MPNS(Base):
    __tablename__ = 'MPNS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    mpn = Column(String)
    datetime_added = Column(DateTime, default=func.current_timestamp()) 

    parts = relationship("Part", secondary="PARTS_MPNS", back_populates="mpns")    

class PartsMPNS(Base):
    __tablename__ = 'PARTS_MPNS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('PARTS.id', ondelete='CASCADE'))
    mpnID = Column(Integer, ForeignKey('MPNS.id', ondelete='CASCADE'))
    datetime_added = Column(DateTime, default=func.current_timestamp()) 


class Product(Base):
    __tablename__ = 'PRODUCTS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_number = Column(String)
    product_description = Column(String)
    division = Column(String)
    datetime_added = Column(DateTime, default=func.current_timestamp()) 

    parts = relationship("Part", secondary="PART_IN_PRODUCT", back_populates="products")
    volumes = relationship("ProductVolumes", back_populates="products")

class PartInProduct(Base):
    __tablename__ = 'PART_IN_PRODUCT'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('PARTS.id', ondelete='CASCADE'))
    productID = Column(Integer, ForeignKey('PRODUCTS.id', ondelete='CASCADE'))
    bom_description=Column(String)
    bom_cost=Column(DECIMAL(12,2),nullable=False,default=0)
    bom_quantity=Column(Float)
    bom_supplier=Column(String)
    export_rating=Column(String)
    datetime_added = Column(DateTime, default=func.current_timestamp()) 

class ProductVolumes(Base):
    __tablename__ = 'PRODUCT_HAS_VOLUMES'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String)
    year = Column(SmallInteger)
    volume=Column(Integer)
    product_id = Column(Integer, ForeignKey('PRODUCTS.id'))

    products = relationship('Product', back_populates="volumes")

class IdeaVolumes(Base):
    __tablename__ = 'IDEA_HAS_VOLUMES'

    id = Column(Integer, primary_key=True, autoincrement=True)
    idea_id = Column(Integer, ForeignKey('IDEAS.id', ondelete='CASCADE'))
    part_cost_id = Column(Integer, ForeignKey('PART_COSTS.id', ondelete='CASCADE'))
    datetime_added = Column(DateTime, default=func.current_timestamp()) 


class PartCosts(Base):
    __tablename__ = 'PART_COSTS'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    part_id = Column(Integer, ForeignKey('PARTS.id'))
    cost = Column(DECIMAL(12,2),default=0.00,nullable=False)
    volume = Column(Integer)
    source = Column(String)    
    type = Column(String, nullable="False")
    datetime_added = Column(DateTime, default=func.current_timestamp()) 

    part = relationship('Part', back_populates="prices")

    ideas_at_volume = relationship("Idea",secondary="IDEA_HAS_VOLUMES", back_populates="volumes")


from constants import dbstring
engine = create_engine(dbstring, echo=True)